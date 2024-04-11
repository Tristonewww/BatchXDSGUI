##Please ignore this part. Path delivery test.
import sys
def main():
    if len(sys.argv) > 1:
        input_path = sys.argv[1]  
        print(f"xdswriter has received input path: {input_path}")
    else:
        print("No input path provided.")

if __name__ == "__main__":
    main()

# XDSwriter.py
import os
import sys

log_file = None

def main(input_path):
    
    global log_file
    
    # Check if input_path is empty    
    if not input_path:
        print("No input path provided. Exiting...")
        sys.exit(1)
    # Traverse the input_path folder and its subdirectories
    for root, dirs, files in os.walk(input_path):
        # Here you can do something with each file
        pass
    # Generate a log file
    log_file = os.path.join(input_path, 'XDSwriter_log.txt')
    with open(log_file, 'w') as f:
        f.write('XDSwriter log file created at ' + input_path + '\n')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        main(input_path)
    else:
        print("No input path provided. Please run the script with an input path.")

folder_path = input_path
# Search for img files
for root, dirs, files in os.walk(folder_path):
    if dirs and dirs[0].lower() == 'xds':
        with open(log_file, 'a') as f:
            f.write(f'{os.path.abspath(root)} folder existed.\n')
        continue  # skip the current directory if xds folder exists
    img_files = [f for f in files if f.lower().endswith('.img')]

    # Img files is enough or not
    if len(img_files) > 3:
        xds_dir = os.path.join(root, 'xds')
        if not os.path.exists(xds_dir):
            os.makedirs(xds_dir)
            xds_inp_file = os.path.join(xds_dir, 'xds.inp')
            with open(xds_inp_file, 'w') as f:
                f.write('! XDS.INP file for Rotation Electron Diffraction - Hongyi and Lei, version April.2023                                                                      \n')
                f.write('!!\n')            
                f.write('! For definitions of input parameters, see:                                                                                                                \n')
                f.write('! http://xds.mpimf-heidelberg.mpg.de/html_doc/xds_parameters.html                                                                                          \n')
                f.write('!!\n')
                f.write('! NOTE: Please convert the tiff files into SMV fomat using RED before processing                                                                           \n')
                f.write('! Images are expected to be already corrected for spatial distortions.                                                                                     \n')
                f.write('!\n')
                f.write('!\n')
                f.write('!\n')
                f.write('!\n')
                f.write('!\n')
                f.write('! ********** Job control **********                                                                                                                        \n')
                f.write('!\n')
                f.write(' !JOB= XYCORR INIT COLSPOT IDXREF                                                                                                                          \n')
                f.write(' !JOB= DEFPIX XPLAN INTEGRATE CORRECT                                                                                                                      \n')
                f.write(' !JOB= CORRECT                                                                                                                                             \n')
                f.write('!\n')
                f.write(' MAXIMUM_NUMBER_OF_JOBS=4                                                                                                                                  \n')
                f.write(' MAXIMUM_NUMBER_OF_PROCESSORS=4                                                                                                                            \n')
                f.write(' !SECONDS=                                                                                                                                                 \n')
                f.write(' !NUMBER_OF_IMAGES_IN_CACHE=                                                                                                                               \n')
                f.write(' !TEST=  !1 : default. Generates the control image FRAME.cbf                                                                                               \n')
                f.write('         !2 : additional diagnostics like overloaded pixels are provided                                                                                   \n')
                f.write('!\n')
                f.write('!\n')
                f.write('! ********** Data images **********                                                                                                                        \n')
                f.write('!\n')
                f.write(' NAME_TEMPLATE_OF_DATA_FRAMES= /00???.img   SMV                                                                                                            \n')
                f.write('!\n')
                f.write(' DATA_RANGE=    \n')
                f.write(' SPOT_RANGE=    \n')
                f.write(' BACKGROUND_RANGE=   \n') 
                f.write(' !EXCLUDE_DATA_RANGE=  24 24                                                                                                                               \n')
                f.write(' !MINIMUM_FRACTION_OF_BACKGROUND_REGION=  !0.01 is default. Rarely needs to be changed.                                                                    \n')
                f.write('!\n')
                f.write('! ********** Crystal **********                                                                                                                            \n')
                f.write('!\n')
                f.write('!SPACE_GROUP_NUMBER=                                                                                                                                        \n')
                f.write('!UNIT_CELL_CONSTANTS=                                                                                                                                       \n')
                f.write(' !UNIT_CELL_A-AXIS=  UNIT_CELL_B-AXIS=  UNIT_CELL_C-AXIS=                                                                                                  \n')
                f.write(' !REIDX=  !Optional reindexing transformation to apply on reflection indices                                                                               \n')
                f.write(" FRIEDEL'S_LAW=TRUE                                                                                                                                        \n")
                f.write(' STARTING_ANGLE= 0                                                                                                                                         \n')
                f.write(' STARTING_FRAME= 1                                                                                                                                         \n')
                f.write(' !phi(i) = STARTING_ANGLE + OSCILLATION_RANGE * (i - STARTING_FRAME)                                                                                       \n')
                f.write('!\n')
                f.write(' !STARTING_ANGLES_OF_SPINDLE_ROTATION=   !used by XPLAN                                                                                                    \n')
                f.write(' !TOTAL_SPINDLE_ROTATION_RANGES=         !used by XPLAN                                                                                                    \n')
                f.write(' !RESOLUTION_SHELLS=                     !used by XPLAN                                                                                                    \n')
                f.write(' !REFERENCE_DATA_SET=                                                                                                                                      \n')
                f.write(' !FIT_B-FACTOR_TO_REFERENCE_DATA_SET=                                                                                                                      \n')
                f.write('!\n')
                f.write(' !MAX_CELL_AXIS_ERROR=         !0.03 is default                                                                                                            \n')
                f.write(' !MAX_CELL_ANGLE_ERROR=        !2.0  is default                                                                                                            \n')
                f.write('!\n')
                f.write(' !TEST_RESOLUTION_RANGE    !for calculation of Rmeas when analysing the intensity data for space group symmetry in the CORRECT step.                       \n')
                f.write(' !MIN_RFL_Rmeas=    !50 is default - used in the CORRECT step for identification of possible space groups.                                                 \n')
                f.write(' !MAX_FAC_Rmeas=    !2.0 is default - used in the CORRECT step for identification of possible space groups.                                                \n')
                f.write('!\n')
                f.write('!\n')
                f.write('! ************************************************                                                                                                         \n')
                f.write('! ********** Detector & Beam parameters **********                                                                                                         \n')
                f.write('!\n')
                f.write('! ********** Detector hardware **********                                                                                                                  \n')
                f.write('!\n')
                f.write(' !DETECTOR=  PILATUS                                                                                                                                       \n')
                f.write('!\n')
                f.write(' NX=   NY=  QX=  QY=  !Number and Size (mm) of pixel                                                                                                       \n')
                f.write('!\n')
                f.write(' OVERLOAD=           !default value dependent on the detector used                                                                                         \n')
                f.write(' !MINIMUM_VALID_PIXEL_VALUE=   !default value dependent on the detector used, 0 in most cases                                                              \n')
                f.write('!\n')
                f.write(' TRUSTED_REGION= 0   1.4142  !default "0.0 1.05". Corners for square detector max "0.0 1.4142"                                                             \n')
                f.write(' !UNTRUSTED_RECTANGLE=                                                                                                                                     \n')
                f.write(' !UNTRUSTED_ELLIPSE=                                                                                                                                       \n')
                f.write(' !UNTRUSTED_QUADRILATERAL=                                                                                                                                 \n')
                f.write('!\n')
                f.write(' ! ??? SILICON=                                                                                                                                            \n')
                f.write(' !SENSOR_THICKNESS=0.30                                                                                                                                    \n')
                f.write('!\n')
                f.write(' !Mark cross as untrusted region (Removing the Cross)                                                                                                      \n')
                f.write(' !UNTRUSTED_RECTANGLE= 255 262 0 517                                                                                                                       \n')
                f.write(' !UNTRUSTED_RECTANGLE= 0 517 255 262                                                                                                                       \n')
                f.write('!\n')
                f.write('!\n')
                f.write('!\n')
                f.write(' !********** Detector distortions **********                                                                                                               \n')
                f.write('!\n')
                f.write(' ! ??? ROFF=     TOFF=                                                                                                                                     \n')
                f.write(' !Radial and tangential offset correction for spiral read-out scanners like MAR or MAC.                                                                    \n')
                f.write(' !At present XDS cannot determine these values and only computes a look-up table of spatial corrections from the given values                              \n')
                f.write(' !(coming from somewhere else). Usually, both values are zero.                                                                                             \n')
                f.write('!\n')
                f.write(' !STOE_CALIBRATION_PARAMETERS=                                                                                                                             \n')
                f.write(' !BRASS_PLATE_IMAGE=                                                                                                                                       \n')
                f.write(' !HOLE_DISTANCE=                                                                                                                                           \n')
                f.write(' !MXHOLE=                                                                                                                                                  \n')
                f.write(' !MNHOLE=                                                                                                                                                  \n')
                f.write('!\n')
                f.write(' ! ??? X-GEO_CORR=                                                                                                                                         \n')
                f.write(' ! ??? Y-GEO_CORR=                                                                                                                                         \n')
                f.write('!\n')
                f.write('! ********** Detector noise **********                                                                                                                     \n')
                f.write('!\n')
                f.write(' ! ??? DARK_CURRENT_IMAGE=                                                                                                                                 \n')
                f.write(' ! ??? OFFSET=                                                                                                                                             \n')
                f.write('!\n')
                f.write('! ********** Trusted detector region **********                                                                                                            \n')
                f.write('!\n')
                f.write(' VALUE_RANGE_FOR_TRUSTED_DETECTOR_PIXELS= 200 300000   ! 6000 30000 is default, for excluding shaded parts of the detector.                                \n')
                f.write(' !MINIMUM_ZETA=   !0.05 is default                                                                                                                         \n')
                f.write('!UNTRUSTED_RECTANGLE= 255 262 0 517                                                                                                                        \n')
                f.write('!UNTRUSTED_RECTANGLE= 0 517 255 262                                                                                                                        \n')
                f.write('!\n')
                f.write(' INCLUDE_RESOLUTION_RANGE=                                                                                                                                 \n')
                f.write('!\n')
                f.write(' !Ice Ring exclusion, important for data collected using cryo holders                                                                                      \n')
                f.write(' !EXCLUDE_RESOLUTION_RANGE=                                                                                                                                \n')
                f.write(' !EXCLUDE_RESOLUTION_RANGE= 3.93 3.87 !ice-ring at 3.897 Angstrom                                                                                          \n')
                f.write('! EXCLUDE_RESOLUTION_RANGE= 3.70 3.64 !ice-ring at 3.669 Angstrom                                                                                          \n')
                f.write(' !EXCLUDE_RESOLUTION_RANGE= 3.47 3.41 !ice-ring at 3.441 Angstrom                                                                                          \n')
                f.write('! EXCLUDE_RESOLUTION_RANGE= 2.70 2.64 !ice-ring at 2.671 Angstrom (Main)                                                                                   \n')
                f.write('! EXCLUDE_RESOLUTION_RANGE= 2.28 2.22 !ice-ring at 2.249 Angstrom (Main)                                                                                   \n')
                f.write(' !EXCLUDE_RESOLUTION_RANGE= 2.102 2.042 !ice-ring at 2.072 Angstrom - strong                                                                               \n')
                f.write(' !EXCLUDE_RESOLUTION_RANGE= 1.978 1.918 !ice-ring at 1.948 Angstrom - weak                                                                                 \n')
                f.write(' !EXCLUDE_RESOLUTION_RANGE= 1.948 1.888 !ice-ring at 1.918 Angstrom - strong                                                                               \n')
                f.write(' !EXCLUDE_RESOLUTION_RANGE= 1.913 1.853 !ice-ring at 1.883 Angstrom - weak                                                                                 \n')
                f.write(' !EXCLUDE_RESOLUTION_RANGE= 1.751 1.691 !ice-ring at 1.721 Angstrom - weak                                                                                 \n')
                f.write('!\n')
                f.write('!\n')
                f.write('! ********** Detector geometry & Rotation axis **********                                                                                                  \n')
                f.write('! see http://xds.mpimf-heidelberg.mpg.de/html_doc/coordinate_systems.html                                                                                  \n')
                f.write('!\n')
                f.write(' DIRECTION_OF_DETECTOR_X-AXIS= 1 0 0                                                                                                                       \n')
                f.write(' DIRECTION_OF_DETECTOR_Y-AXIS= 0 1 0                                                                                                                       \n')
                f.write('!\n')
                f.write(' !Detector origin (pixels). Often close to the image center, i.e. ORGX=NX/2; ORGY=NY/2                                                                     \n')
                f.write(' ORGX=  ORGY=                                                                                                                                              \n')
                f.write(' ! can be negative. Positive because the detector normal points away from the crystal.                                                                     \n')
                f.write(' DETECTOR_DISTANCE=                                                                                                                                        \n')
                f.write('!\n')
                f.write(' OSCILLATION_RANGE=                                                                                                                                        \n')
                f.write(' !XDS assumes a right handed rotation of the crystal about the rotation axis when proceeding to the next data image.                                       \n')
                f.write('!\n')
                f.write(' ROTATION_AXIS=   !cos(155.3) cos(65.3)  !in XDS.INP emailed: 0.078605 0.996888 -0.005940                                                                  \n')
                f.write('!\n')
                f.write(' !Nota on Rotation Axis: Direction cosines of the rotation axis with respect to the laboratory system.                                                     \n')
                f.write(' !The length of this vector will be normalized by XDS.                                                                                                     \n')
                f.write(' !The direction of the axis is chosen to describe a right-handed rotation.                                                                                 \n')
                f.write(' !Example:ROTATION_AXIS= 0.0 1.0 0.0                                                                                                                       \n')
                f.write(' !The rotation axis points along the laboratory y-axis. When looking along the axis,                                                                       \n')
                f.write(' !the crystal would rotate clockwise when proceeding to the next data image.                                                                               \n')
                f.write(' !Often "1 0 0" at synchrotron                                                                                                                             \n')
                f.write('!\n')
                f.write(' !SEGMENT=                                                                                                                                                 \n')
                f.write(' !REFINE_SEGMENT=                                                                                                                                          \n')
                f.write(' !DIRECTION_OF_SEGMENT_X-AXIS=                                                                                                                             \n')
                f.write(' !DIRECTION_OF_SEGMENT_Y-AXIS=                                                                                                                             \n')
                f.write(' !SEGMENT_ORGX=                                                                                                                                            \n')
                f.write(' !SEGMENT_ORGY=                                                                                                                                            \n')
                f.write(' !SEGMENT_DISTANCE=                                                                                                                                        \n')
                f.write('!\n')
                f.write('!\n')
                f.write('! ********** Incident beam **********                                                                                                                      \n')
                f.write('!\n')
                f.write(' X-RAY_WAVELENGTH=       !used by IDXREF                                                                                                                   \n')
                f.write(' INCIDENT_BEAM_DIRECTION= 0 0 1  !used by IDXREF +CORRECT(?) ???? (REC. ANGSTROM)  !The vector points from the source towards the crystal                  \n')
                f.write('!\n')
                f.write(' ! ??? FRACTION_OF_POLARIZATION=     !0.5 is default, for unpolarized beam                                                                                 \n')
                f.write(' !Fraction of polarization of direct beam in a plane specified by its normal. (0 < FRACTION_OF_POLARIZATION < 1).                                          \n')
                f.write(' !For a negative value of FRACTION_OF_POLARIZATION or a value larger than 1 no polarization correction is carried out.                                     \n')
                f.write('!\n')
                f.write(' ! ??? POLARIZATION_PLANE_NORMAL=                                                                                                                          \n')
                f.write(' !x, y, z components of the polarization plane normal with respect to the laboratory coordinate system.                                                    \n')
                f.write(' !Example :                                                                                                                                                \n')
                f.write(' !FRACTION_OF_POLARIZATION=0.95                                                                                                                            \n')
                f.write(' !POLARIZATION_PLANE_NORMAL= 0.0 1.0 0.0                                                                                                                   \n')
                f.write(' !The electrical field vector of the incident beam is found in the x,z-plane of the laboratory coordinate system with a probability of 0.95.               \n')
                f.write('!\n')
                f.write(' ! ??? AIR=                                                                                                                                                \n')
                f.write(' !Fraction of intensity loss per mm due to air absorption. The absorption of x-rays by air depends on the wavelength.                                      \n')
                f.write(' !XDS will provide the appropriate value unless specified by the user.                                                                                     \n')
                f.write('!\n')
                f.write('!\n')
                f.write('! ********** Background and peak pixels **********                                                                                                         \n')
                f.write('!\n')
                f.write(' !NBX=     NBY=                         !3 is default                                                                                                      \n')
                f.write('! BACKGROUND_PIXEL=20                     !6.0 is default                                                                                                  \n')
                f.write('!STRONG_PIXEL= 5.0                       !3.0 is default                                                                                                   \n')
                f.write(' !MAXIMUM_NUMBER_OF_STRONG_PIXELS=      !1500000 is default                                                                                                \n')
                f.write(' !MINIMUM_NUMBER_OF_PIXELS_IN_A_SPOT=3   !6 is default         ?????                                                                                       \n')
                f.write(' !SPOT_MAXIMUM-CENTROID=                !2.0 is default                                                                                                    \n')
                f.write('! SIGNAL_PIXEL=6                         !3.0 is default                                                                                                   \n')
                f.write('!\n')
                f.write('!\n')
                f.write('! ********************************                                                                                                                         \n')
                f.write('! ********** Refinement **********                                                                                                                         \n')
                f.write('!\n')
                f.write(' REFINE(IDXREF)= AXIS ORIENTATION CELL  BEAM  !POSITION BEAM AXIS       !ORIENTATION CELL !SEGMENT!                                                        \n')
                f.write(' REFINE(INTEGRATE)= !POSITION BEAM AXIS       !ORIENTATION CELL                                                                                            \n')
                f.write(' REFINE(CORRECT)= ORIENTATION CELL AXIS  BEAM  !POSITION BEAM AXIS ORIENTATION CELL        !SEGMENT                                                        \n')
                f.write(' ! Parameter Keywords:                                                                                                                                     \n')
                f.write(' !POSITION - refine the position of the origin of the detector system                                                                                      \n')
                f.write(' !BEAM - refine direct beam direction                                                                                                                      \n')
                f.write(' !AXIS - refine rotation axis                                                                                                                              \n')
                f.write(' !ORIENTATION - refine unit cell orientation                                                                                                               \n')
                f.write(' !CELL - refine unit cell constants                                                                                                                        \n')
                f.write(' !SEGMENT - refine internal segment assembly of the detector                                                                                               \n')
                f.write(' ! Nota: "ALL" does not work in XDS version July 2016                                                                                                      \n')
                f.write('!\n')
                f.write(' !DEFAULT_REFINE_SEGMENT=                                                                                                                                  \n')
                f.write(' !MINIMUM_NUMBER_OF_REFLECTIONS/SEGMENT=                                                                                                                   \n')
                f.write('!\n')
                f.write('!\n')
                f.write('! *********************************************                                                                                                            \n')
                f.write('! ********** Processing Optimization **********                                                                                                            \n')
                f.write('!\n')
                f.write('! ********** Indexing **********                                                                                                                           \n')
                f.write('!\n')
                f.write(' !INDEX_ORIGIN=      !0 0 0 is default. Used by IDXREF to add an index offset                                                                              \n')
                f.write(' !INDEX_ERROR=       !0.05 is default                                                                                                                      \n')
                f.write(' !INDEX_MAGNITUDE=   !8 is default                                                                                                                         \n')
                f.write(' !INDEX_QUALITY=     !0.8 is default                                                                                                                       \n')
                f.write('!\n')
                f.write('!\n')
                f.write(' ! SEPMIN=2.0            !6.0 is default, hardly needs to be changed                                                                                       \n')
                f.write(' ! CLUSTER_RADIUS=2    !3 is default, hardly needs to be changed.                                                                                          \n')
                f.write('!\n')
                f.write(' !MAXIMUM_ERROR_OF_SPOT_POSITION=       !3.0 is default, hardly needs to be changed.                                                                       \n')
                f.write(' !MAXIMUM_ERROR_OF_SPINDLE_POSITION=    !2.0 is default, hardly needs to be changed.                                                                       \n')
                f.write('!\n')
                f.write(' MINIMUM_FRACTION_OF_INDEXED_SPOTS= 0.25    !0.50 is default.                                                                                              \n')
                f.write('!\n')
                f.write('!\n')
                f.write('! ********** Peak profiles and Integration **********                                                                                                      \n')
                f.write('!\n')
                f.write(' !REFLECTING_RANGE=                                                                                                                                        \n')
                f.write(' !REFLECTING_RANGE_E.S.D.= 0.466                                                                                                                           \n')
                f.write(' !BEAM_DIVERGENCE=                                                                                                                                         \n')
                f.write('!BEAM_DIVERGENCE_E.S.D.=0.004                                                                                                                              \n')
                f.write(' !Definitions:                                                                                                                                             \n')
                f.write(' !REFLECTING_RANGE=                                                                                                                                        \n')
                f.write(' !Angular life time (degrees) of a reflection to pass completely through the Ewald sphere on shortest route.                                               \n')
                f.write(' !The parameter value controls the raster size along gamma of the reflection profiles in step "INTEGRATE".                                                 \n')
                f.write(' !A slightly larger value should be specified to include some background from adjacent data images.                                                        \n')
                f.write(' !Parameter is used by COLSPOT, IDXREF, INTEGRATE                                                                                                          \n')
                f.write(' !REFLECTING_RANGE_E.S.D.=                                                                                                                                 \n')
                f.write(' !Describes the mosaicity (degrees) of the crystal.                                                                                                        \n')
                f.write(' !Parameter is used by INTEGRATE                                                                                                                           \n')
                f.write(' !BEAM_DIVERGENCE=                                                                                                                                         \n')
                f.write(' !This value is approximately arctan(spot diameter/DETECTOR_DISTANCE) in degrees.                                                                          \n')
                f.write(' !The parameter value defines the raster size along alpha/beta of the reflection profiles.                                                                 \n')
                f.write(' !A slightly larger value should be given to include some background pixels around each spot.                                                              \n')
                f.write(' !To compute the spot diameter you need the pixel lengths (QX=, QY=) in mm.                                                                                \n')
                f.write(' !Example: 0.10, the value defines the solid angle of a diffraction spot in degrees.                                                                       \n')
                f.write(' !Parameter is used by INTEGRATE                                                                                                                           \n')
                f.write(' !BEAM_DIVERGENCE_E.S.D.=                                                                                                                                  \n')
                f.write(' !Defines the standard deviation of BEAM_DIVERGENCE=.                                                                                                      \n')
                f.write(' ! Nota:                                                                                                                                                   \n')
                f.write(' !If any of these 4 parameters is left unspecified by the user, all these values will be determined automatically from the data images.                    \n')
                f.write('!\n')
                f.write('!\n')
                f.write(' NUMBER_OF_PROFILE_GRID_POINTS_ALONG_ALPHA/BETA=13    !9 is default                                                                                        \n')
                f.write(' !NUMBER_OF_PROFILE_GRID_POINTS_ALONG_GAMMA=         !9 is default                                                                                         \n')
                f.write(' ! Each reflection when mapped to the surface of the Ewald sphere is sampled by 9 x 9 raster points in the plane tangential to the sphere                  \n')
                f.write(' ! and by 9 points along the shortest rotation route through the sphere.                                                                                   \n')
                f.write('!\n')
                f.write(' !CUT=        !2.0 is default. Grid points in the reflection profile less than 2% of the maximum are not used for integration.                             \n')
                f.write(' ! used by INTEGRATE                                                                                                                                       \n')
                f.write(' !DELPHI=     !5.0 is default = 5 degrees of spindle rotation.                                                                                             \n')
                f.write(' ! If there are too few strong spots which could be used for learning spot profiles, it may be useful to specify a larger value.                           \n')
                f.write(' ! used by INTEGRATE                                                                                                                                       \n')
                f.write('!\n')
                f.write(' !MINPK=   !75.0 is default, hardly needs to be changed.                                                                                                   \n')
                f.write(' ! Defines the minimum required percentage of observed reflection intensity.                                                                               \n')
                f.write('!\n')
                f.write(' !WFAC1=   !1.0 is default, hardly needs to be changed.                                                                                                    \n')
                f.write(' ! used for recognizing MISFITS. A larger value, like 1.5, would reduce the number of MISFITS (and increase the R-factors).                                \n')
                f.write('!\n')
                f.write(' !PROFILE_FITTING=    !TRUE is default                                                                                                                     \n')
                f.write('!\n')
                f.write('! ********** Correction factors **********                                                                                                                 \n')
                f.write('!\n')
                f.write(' !STRICT_ABSORPTION_CORRECTION=    !FALSE is default                                                                                                       \n')
                f.write(' !PATCH_SHUTTER_PROBLEM=           !FALSE is default                                                                                                       \n')
                f.write(' !CORRECTIONS=                     !DECAY MODULATION ABSORPTION  !ALL is default                                                                           \n')
                f.write(' !MINIMUM_I/SIGMA=                 !3.0 is default. For determination of correction factors.                                                               \n')
                f.write(' !NBATCH=                          !XDS will determine a reasonable value                                                                                  \n')
                f.write(' !REFLECTIONS/CORRECTION_FACTOR=                                                                                                                           \n')
                f.write(' !REJECT_ALIEN=                    !20.0 is default                                                                                                        \n')
                f.write(' !DATA_RANGE_FIXED_SCALE_FACTOR=                                                                                                                           \n')
                f.write('!\n')

            with open(log_file, 'a') as f:                                                                                                                                         
                f.write(f'{os.path.abspath(root)} xds created.\n')                                                                                                                 
        else:                                                                                                                                                                      
            with open(log_file, 'a') as f:                                                                                                                                         
                f.write(f'{os.path.abspath(root)} folder existed.\n')                                                                                                              

print('Files created successfully')                        

# update xds.inp

xds_inp_files = []
img_only_folders = []

for root, dirs, files in os.walk(folder_path):
    img_files = [f for f in files if f.lower().endswith('.img')]
    if img_files:
        if any(file.lower() == 'xds.inp' for file in files):
            xds_inp_files.append(os.path.join(root, 'xds.inp'))
        else:
            img_only_folders.append(os.path.abspath(root))

xds_inp_files = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.lower() == 'xds.inp':
            xds_inp_files.append(os.path.join(root, file))

for xds_inp_file in xds_inp_files:
    current_path = os.path.dirname(xds_inp_file)
    parent_path = os.path.dirname(current_path)
    image_count = len([f for f in os.listdir(parent_path) if f.lower().endswith('.img')])

    with open(xds_inp_file, 'r') as f:
        xds_inp_lines = f.readlines()

    keywords = ["NAME_TEMPLATE_OF_DATA_FRAMES=", "DATA_RANGE=", "SPOT_RANGE=", "BACKGROUND_RANGE="]
    found = [False] * len(keywords)
    for i, line in enumerate(xds_inp_lines):
        if not all(found):
            for j, keyword in enumerate(keywords):
                if line.strip().startswith(keyword):
                    found[j] = True
                    if keyword == "NAME_TEMPLATE_OF_DATA_FRAMES=":
                        first_img_file = next(f for f in os.listdir(parent_path) if f.lower().endswith('.img'))
                        first_img_file_no_ext = first_img_file[:-4]
                        modified_img_file_no_ext = first_img_file_no_ext[:-4]
                        new_line = f"{keyword}{parent_path}/{modified_img_file_no_ext}????.img   SMV\n"
                        new_line = new_line.replace("\\", "/")
                        xds_inp_lines[i] = new_line
                    elif keyword in ["DATA_RANGE=", "SPOT_RANGE=", "BACKGROUND_RANGE="]:
                        new_line = f"{keyword}  1  {image_count - 1}\n"
                        xds_inp_lines[i] = new_line
                    break

    if all(found):
        with open(xds_inp_file, 'w') as f:
            f.writelines(xds_inp_lines)
    else:
        with open(log_file, 'a') as f:
            f.write(f"xdsinp is not complete in {os.path.abspath(os.path.dirname(xds_inp_file))}\n")
            
print("All frame number and path modified successfully.")            



#####update experiment information

# Initialize settings to None
settings = None

# Check if an input path is provided
if len(sys.argv) > 1:
    input_path = sys.argv[1]

    # Construct the path to 'Input_parameters.txt'
    file_path = os.path.join(input_path, 'Input_parameters.txt')

    # Check if the file exists
    if not os.path.isfile(file_path):
        print("The specified file (Input_parameters.txt) does not exist.")
        sys.exit(1)

    # Read the file
    with open(file_path, 'r') as f:
        settings = f.readlines()
else:
    print("No input path provided. Please run the script with an input path.")
    sys.exit(1)

# Ensure that settings were successfully read
if settings is None:
    print("Failed to read settings from the file.")
    sys.exit(1)

nx = None
overload = None
include_resolution_range = None
orgx = None
detector_distance = None
oscillation_range = None
rotation_axis = None
xray_wavelength = None

for line in settings:
    if line.strip().lower().startswith("nx="):
        nx = line.strip()
    elif line.strip().lower().startswith("overload="):
        overload = line.strip()
    elif line.strip().lower().startswith("include_resolution_range="):
        include_resolution_range = line.strip()
    elif line.strip().lower().startswith("orgx="):
        orgx = line.strip()
    elif line.strip().lower().startswith("detector_distance="):
        detector_distance = line.strip()
    elif line.strip().lower().startswith("oscillation_range="):
        oscillation_range = line.strip()
    elif line.strip().lower().startswith("rotation_axis="):
        rotation_axis = line.strip()
    elif line.strip().lower().startswith("x-ray_wavelength="):
        xray_wavelength = line.strip()

# Check if all settings are complete
if nx is None or overload is None or include_resolution_range is None or orgx is None or detector_distance is None or oscillation_range is None or rotation_axis is None or xray_wavelength is None:
    print("Settings are not complete.")
    exit()

# Traverse through the folders and modify the XDS input files
xds_inp_files = []
img_only_folders = []

for root, dirs, files in os.walk(folder_path):
    img_files = [f for f in files if f.lower().endswith('.img')]
    if img_files:
        if any(file.lower() == 'xds.inp' for file in files):
            xds_inp_files.append(os.path.join(root, 'xds.inp'))
        else:
            img_only_folders.append(os.path.abspath(root))

xds_inp_files = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.lower() == 'xds.inp':
            xds_inp_files.append(os.path.join(root, file))

for xds_inp_file in xds_inp_files:
    current_path = os.path.dirname(xds_inp_file)
    parent_path = os.path.dirname(current_path)
    image_count = len([f for f in os.listdir(parent_path) if f.lower().endswith('.img')])

    with open(xds_inp_file, 'r') as f:
        xds_inp_lines = f.readlines()

    keywords = ["NAME_TEMPLATE_OF_DATA_FRAMES=", "DATA_RANGE=", "SPOT_RANGE=", "BACKGROUND_RANGE=", "NX=", "OVERLOAD=", "INCLUDE_RESOLUTION_RANGE=", "ORGX=", "DETECTOR_DISTANCE=", "OSCILLATION_RANGE=", "ROTATION_AXIS=", "X-RAY_WAVELENGTH="]
    found = [False] * len(keywords)
    for i, line in enumerate(xds_inp_lines):
        if not all(found):
            for j, keyword in enumerate(keywords):
                if line.strip().lower().startswith(keyword.lower()):
                    found[j] = True
                    if keyword.lower() == "name_template_of_data_frames=":
                        first_img_file = next(f for f in os.listdir(parent_path) if f.lower().endswith('.img'))
                        first_img_file_no_ext = first_img_file[:-4]
                        modified_img_file_no_ext = first_img_file_no_ext[:-4]
                        new_line = f"{keyword}{parent_path}/{modified_img_file_no_ext}0???.img   SMV\n"
                        new_line = new_line.replace("\\", "/")
                        xds_inp_lines[i] = new_line
                    elif keyword.lower() in ["data_range=", "spot_range=", "background_range="]:
                        new_line = f"{keyword}  1  {image_count - 1}\n"
                        xds_inp_lines[i] = new_line
                    elif keyword.lower() == "nx=":
                        xds_inp_lines[i] = nx + "\n"
                    elif keyword.lower() == "overload=":
                        xds_inp_lines[i] = overload + "\n"
                    elif keyword.lower() == "include_resolution_range=":
                        xds_inp_lines[i] = include_resolution_range + "\n"
                    elif keyword.lower() == "orgx=":
                        xds_inp_lines[i] = orgx + "\n"
                    elif keyword.lower() == "detector_distance=":
                        xds_inp_lines[i] = detector_distance + "\n"
                    elif keyword.lower() == "oscillation_range=":
                        xds_inp_lines[i] = oscillation_range + "\n"
                    elif keyword.lower() == "rotation_axis=":
                        xds_inp_lines[i] = rotation_axis + "\n"
                    elif keyword.lower() == "x-ray_wavelength=":
                        xds_inp_lines[i] = xray_wavelength + "\n"
                    break

    if all(found):
        with open(xds_inp_file, 'w') as f:
            f.writelines(xds_inp_lines)
    else:
        with open(log_file, 'a') as f:
            f.write(f"xdsinp is not complete in {os.path.abspath(os.path.dirname(xds_inp_file))}\n")

print("All TEM and camera information modified successfully.")

# Read the input file and get the settings for Beamstop_start and Beamstop_end line
beamstop_start_line = None
beamstop_end_line = None
beamstop_content = ""

with open(file_path, 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip().lower() == "beamstop_start":
        beamstop_start_line = i
    elif line.strip().lower() == "beamstop_end":
        beamstop_end_line = i
        break

if beamstop_start_line is not None and beamstop_end_line is not None:
    beamstop_content = "".join(lines[beamstop_start_line+1:beamstop_end_line])
else:
    print("Beamstop_start and/or Beamstop_end not found in the input file.")
    exit()

# Traverse through the folders and find XDS input files
xds_inp_files = []

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.lower() == 'xds.inp':
            xds_inp_files.append(os.path.join(root, file))

# Append Beamstop content to all XDS input files
for xds_inp_file in xds_inp_files:
    with open(xds_inp_file, 'a') as f:
        f.write(beamstop_content)
    
# Read the input file and get the settings for toggle
Toggle_start_line = None
Toggle_end_line = None
Toggle_content = ""

file_path = os.path.join(input_path, 'Input_parameters.txt')
with open(file_path, 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.strip().lower() == "toggle_on":
        Toggle_start_line = i
    elif line.strip().lower() == "toggle_off":
        Toggle_end_line = i
        break

if Toggle_start_line is not None and Toggle_end_line is not None:
    Toggle_content = "".join(lines[Toggle_start_line+1:Toggle_end_line])
    # Float content
    try:
        toggle_frame_value = float(Toggle_content.strip())
    except ValueError:
        print("Toggle_content does not contain a valid float.")
        exit()
else:
    print("Toggle_on and/or Toggle_off not found in the input file.")
    exit()

# Traverse through the folders and find XDS input files
xds_inp_files = []

for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.lower() == 'xds.inp':
            xds_inp_files.append(os.path.join(root, file))

# Function to extract image count toggle from XDS input file
def get_image_count_toggle(xds_inp_file):
    with open(xds_inp_file, 'r') as f:
        for line in f:
            if line.startswith("SPOT_RANGE="):
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        return float(parts[2])  # Return the second float value following SPOT_RANGE=
                    except ValueError:
                        print(f"Could not convert {parts[2]} to float in {xds_inp_file}")
                        return None
    return None

# Append toggle content to all XDS input files
for xds_inp_file in xds_inp_files:
    image_count_toggle = get_image_count_toggle(xds_inp_file)
    if image_count_toggle is not None:
        with open(xds_inp_file, 'a') as f:
            toggle_i = 1
            while toggle_frame_value * toggle_i <= image_count_toggle:
                exclude_range_value = int(toggle_frame_value * toggle_i)
                f.write(f"EXCLUDE_DATA_RANGE={exclude_range_value} {exclude_range_value}\n")
                toggle_i += 1

print("All toggle information modified successfully.")

print("All Beamstop information modified successfully.")