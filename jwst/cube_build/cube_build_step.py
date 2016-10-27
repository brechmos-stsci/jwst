 #! /usr/bin/env python

import sys
import time
import json
import numpy as np
from ..stpipe import Step, cmdline
from .. import datamodels
from . import cube_build_io
from . import cube_build
from . import cube
from . import CubeCloud
from . import cube_model
from . import InstrumentDefaults
from . import coord
1
class CubeBuildStep (Step):
    """
    CubeBuildStep: Creates a 3-D spectral cube from a given association or single input file
    The association will contain which channel/subchannel (MIRI) or filter/grating (NIRSPEC)
    the IFU Cube is going to cover. 
    """

    spec = """
         channel = string(default='')
         band   = string(default='')
         grating   = string(default='')
         filter   = string(default='')
         scale1 = float(default=0.0)
         scale2 = float(default =0.0)
         scalew = float(default = 0.0)
         interpolation = option(,'pointcloud','area',default='pointcloud')
         weighting = option('standard','miripsf',default = 'standard')
         coord_system = option('ra-dec','alpha-beta',default='ra-dec')
         roi1 = float(default=1.0)
         roi2 = float(default=1.0)
         roiw = float(default=1.0)
         offset_list = string(default='NA')

       """

    def process(self, input):
        self.log.info('Starting IFU Cube Building Step 2...')

        self.subchannel = self.band

        if(not self.subchannel.isupper()): self.subchannel = self.subchannel.upper()
        if(not self.filter.isupper()): self.filter = self.filter.upper()
        if(not self.grating.isupper()): self.grating = self.grating.upper()
        if(not self.coord_system.islower()): self.coord_system = self.coord_system.lower()
        if(not self.interpolation.islower()): self.interpolation = self.interpolation.lower()
        if(not self.weighting.islower()): self.weighting = self.weighting.lower()
        if(self.channel != ''): self.log.info('Input Channel %s', self.channel)
        if(self.subchannel != ''): self.log.info('Input Channel %s', self.subchannel)
        if(self.grating != ''): self.log.info('Input Channel %s', self.grating)
        if(self.filter != ''): self.log.info('Input Channel %s', self.filter)
        if(self.scale1 != 0.0): self.log.info('Input Scale of axis 1 %f', self.scale1)
        if(self.scale2 != 0.0): self.log.info('Input Scale of axis 2 %f', self.scale2)
        if(self.scalew != 0.0): self.log.info('Input wavelength scale %f  ', self.scalew)
        if(self.offset_list != 'NA'): self.log.info('Offset Dither list %s', self.offset_list)

        # valid coord_system:
        # 1. alpha-beta (only valid for MIRI Single Cubes)
        # 2. ra-dec

        if (self.interpolation == 'area'):
            self.coord_system = 'alpha-beta'

        if (self.coord_system == 'ra-dec'):
            self.interpolation = 'pointcloud'  # can not be area

        self.log.info('Input interpolation %s', self.interpolation)

        self.log.info('Coordinate system to use %s', self.coord_system)
        self.log.info('Weighting method for point cloud %s',self.weighting)
#_________________________________________________________________________________________________
# Set up the IFU cube basic parameters that define a cube
        self.metadata = {}
        self.metadata['instrument'] = ''
        self.metadata['detector'] = ''
        self.metadata['num_bands'] = 0 

        self.metadata['channel'] = list()     # input parameter or determined from reading in files
        self.metadata['subchannel'] = list()  # inputparameter or determined from reading in files 

        self.metadata['band_channel'] = list()     # band channel: 1-1 pairing with band_subchannel
        self.metadata['band_subchannel'] = list()  # band subchannel: 1-1 pairing with band_channel
 
        self.metadata['filter'] = list()   # input parameter
        self.metadata['grating'] = list()  # input parameter

        self.metadata['band_filter'] = list()   # band filter: 1-1 pairing with band_grating 
        self.metadata['band_grating'] = list()  # band grating: 1-1 pairing with band_filter

        self.metadata['output_name'] = ''
        self.metadata['number_files'] = 0

        # input read parameters - Channel, Band (Subchannel), Grating, Filter
        cube_build_io.Read_User_Input(self)

#_________________________________________________________________________________________________
        #Read in the input data - either in form of ASSOCIATION table or single filename
        # If a single file - then assocation table format is filled in

        input_table = cube_build_io.IFUCubeASN(input)

        self.input_table_type = 'Association'
        if(input_table.asn_table['asn_type'] == 'singleton'):
            self.offset_list = 'NA'
            self.input_table_type = 'singleton'

        self.log.debug('Output Base %s ', input_table.asn_table['products'][0]['name'])

        # Check if there is an offset list (this ra,dec dither offset list will probably
        # only be used in testing) 
        self.ra_offset = list()  # units arc seconds
        self.dec_offset = list() # units arc seconds
        if(self.offset_list != 'NA'):
            print('Going to read in dither offset list')
            cube_build_io.ReadOffSetFile(self)

        # Read in the input data (association table or single file)
        # Fill in MasterTable   based on Channel/Subchannel  or filter/grating
        # Also if there is an Offset list - fill in MasterTable.FileOffset
        MasterTable = cube_build_io.FileTable()
        
        num, instrument,detector = cube_build_io.SetFileTable(self, input_table, 
                                                              MasterTable)

        self.metadata['number_files'] = num
        self.metadata['detector'] = detector            
        self.metadata['instrument'] = instrument

        # Determine which channels/subchannels or filter/grating cubes will be constructed from.
        # returns self.metadata['subchannel'] and self.metadata['channel']
        # or self.metadata['filter'], self.metadata['grating']

        cube_build_io.DetermineCubeCoverage(self, MasterTable)
        cube_build.CheckCubeType(self)


        self.output_name_base = input_table.asn_table['products'][0]['name']

        self.output_name = cube_build_io.UpdateOutPutName(self)

#________________________________________________________________________________

# Cube is an instance of CubeInfo - which holds basic information on Cube
# Set up if we are building a MIRI cube or a NIRSPEC cube

        if(instrument == 'MIRI'):
            Cube = cube.CubeInfo('MIRI',detector,
                                 self.metadata['band_channel'], 
                                 self.metadata['band_subchannel'], 
                                 self.output_name)

        if(instrument == 'NIRSPEC'):
            Cube = cube.CubeInfo('NIRSPEC',detector,
                                 self.metadata['band_filter'], 
                                 self.metadata['band_grating'], 
                                 self.output_name)


        # for now InstrumentDefaults holds defaults on the two instruments
        InstrumentInfo = InstrumentDefaults.Info() 
        self.log.info(' Building Cube %s ', Cube.output_name)


            # Scale is 3 dimensions and is determined from default values InstrumentInfo.GetScale
        scale = cube_build.DetermineScale(Cube, InstrumentInfo)

            # if the user has set the scale of output cube use those values instead
        a_scale = scale[0]
        if self.scale1 != 0:
            a_scale = self.scale1

        b_scale = scale[1]
        if self.scale2 != 0:
            b_scale = self.scale2

        wscale = scale[2]
        if self.scalew != 0:
            wscale = self.scalew

        Cube.SetScale(a_scale, b_scale, wscale)

        t0 = time.time()
#________________________________________________________________________________
# find the min & max final coordinates of cube: map each slice to cube
# add any dither offsets, then find the min & max value in each dimension
# Foot print is returned in ra,dec coordinates


        CubeFootPrint = cube_build.DetermineCubeSize(self, Cube, 
                                                         MasterTable, 
                                                         InstrumentInfo)

        t1 = time.time()
        print("Time to determine size of cube = %.1f.s" % (t1 - t0,))

            # Based on Scaling and Min and Max values determine naxis1, naxis2, naxis3
            # set cube CRVALs, CRPIXs and xyz coords (center  x,y,z vector spaxel centers)
        if(self.coord_system == 'ra-dec'): 
            Cube.SetGeometry(CubeFootPrint)
        else: 
            Cube.SetGeometryAB(CubeFootPrint) # local coordinate system 

        Cube.PrintCubeGeometry(instrument)

            # if the user has not set the size of the ROI then use defaults of 1* cube scale in dimension
        if(self.roi1 == 1): self.roi1 = Cube.Cdelt1* 1.0
        if(self.roi2 == 1): self.roi2 = Cube.Cdelt2* 1.0
        if(self.roiw == 1): self.roiw = Cube.Cdelt3* 1.0

            # for now keep these values - may not use them in the future
        self.power_x = 1
        self.power_y = 1
        self.power_z = 1


        IFUCube = cube_model.SetUpIFUCube(Cube)

        if(self.interpolation == 'pointcloud'):
            self.log.info('Region of interest %f %f %f', 
                              self.roi1, self.roi2, self.roiw)
            self.log.info('Power parameters for weighting %5.1f %5.1f %5.1f', 
                              self.power_x, self.power_y, self.power_z)

            # now you have the size of cube - create an instance for each spaxel
            # create an empty spaxel list - this will become a list of Spaxel classses
        spaxel = []

            # set up center of the corner cube spaxel
        t0 = time.time()
        for z in range(Cube.naxis3):
            for y in range(Cube.naxis2):
                for x in range(Cube.naxis1):
                    spaxel.append(cube.Spaxel(Cube.xcoord[x], 
                                              Cube.ycoord[y], 
                                              Cube.zcoord[z]))                        
        t1 = time.time()
        print("Time to create list of spaxel classes = %.1f.s" % (t1 - t0,))

        # create an empty Pixel Cloud array of 10 columns
        # if doing interpolation on point cloud this will become a matrix of  Pixel Point cloud values
        # each row holds information for a single pixel

        # Initialize the PixelCloud to 10   columns of zeros (1 row)
        PixelCloud = np.zeros(shape=(10, 1))
        t0 = time.time()
        # now need to loop over every file that covers this channel/subchannel (MIRI) or Grating/filter(NIRSPEC)
        #and map the detector pixels to the cube spaxel.
        if(instrument == 'MIRI'):
            parameter1 = Cube.channel
            parameter2 = Cube.subchannel
        elif(instrument == 'NIRSPEC'):
            parameter1 = Cube.grating
            parameter2 = Cube.filter

        number_bands = len(parameter1)
        for i in range(number_bands):
            this_par1 = parameter1[i]
            this_par2 = parameter2[i]            
            
            self.log.info("Working on Band defined by:%s %s " ,this_par1,this_par2)

            PixelCloud = cube_build.MapDetectorToCube(self, 
                                                      this_par1, this_par2, 
                                                      Cube, spaxel, 
                                                      MasterTable,
                                                      InstrumentInfo,
                                                      IFUCube)

        t1 = time.time()
        self.log.info("Time Map All slices on Detector to Cube = %.1f.s" % (t1 - t0,))

#_______________________________________________________________________
# Mapped all data to cube or Point Cloud
# now determine Cube Spaxel flux

        t0 = time.time()
        if self.interpolation == 'pointcloud':
            CubeCloud.FindROI(self, Cube, spaxel, PixelCloud)
        t1 = time.time()
        self.log.info("Time to find the ROI = %.1f.s" % (t1 - t0,))


        t0 = time.time()
        cube_build.FindCubeFlux(self, Cube, spaxel, PixelCloud)

        t1 = time.time()
        self.log.info("Time find Cube Flux= %.1f.s" % (t1 - t0,))
# write out the IFU cube
#        IFUcubeModel = cube_build_io.WriteCube(self, Cube, spaxel)
        IFUCube = cube_model.UpdateIFUCube(self, Cube,IFUCube, spaxel)




if __name__ == '__main__':
    cmdline.step_script( cube_build_step )
