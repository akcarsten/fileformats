import numpy as np
import pandas as pd
import shutil
import os


def run_fileformats():
    """ At the moment no input arguments.
    This function creates a random data set, saves it in different file formats and returns the file sizes."""

    output_folder = './tmp'
    output_file_base = '{}/size_test.'.format(output_folder)

    data_format = np.dtype([('time', np.uint64),
                            ('setPressure', np.uint32),
                            ('setTemperature', np.int8),
                            ('setVoltage', np.float32),
                            ('setAsicOdr', np.uint8),
                            ('dutPressure', np.float64),
                            ('dutTemperature', np.float32),
                            ('dutAdcPressure', np.float64),
                            ('dutAdcTemperature', np.float64)
                            ])

    if os.path.isdir(output_folder) is False:
        os.mkdir(output_folder)

    dummy_data = np.recarray((100000,), dtype=data_format)

    for name in dummy_data.dtype.names:
        dummy_data[name] = np.random.normal(1, 3, dummy_data.shape)

    # Save as binary
    output_file = output_file_base + 'bytes'
    fid = open(output_file, 'wb')
    fid.write(dummy_data.tobytes())
    fid.close()
    print("Size binary: " + str(os.path.getsize(output_file) / 1000000) + "MB")

    # Save as string
    output_file = output_file_base + 'string'
    fid = open(output_file, 'w')
    fid.write(str(dummy_data.tolist()))
    fid.close()
    print("Size string: " + str(os.path.getsize(output_file) / 1000000) + "MB")

    # Save as HDF5
    output_file = output_file_base + 'hdf5'
    df = pd.DataFrame(dummy_data)
    df.to_hdf(output_file, key='df', mode='w', format='table')
    print("Size HDF5: " + str(os.path.getsize(output_file) / 1000000) + "MB")


    # Save as Parquet
    output_file = output_file_base + 'parquet'
    df = pd.DataFrame(dummy_data)
    df.to_parquet(output_file, compression='GZIP')
    print("Size Parquet: " + str(os.path.getsize(output_file) / 1000000) + "MB")

    shutil.rmtree(output_folder)


if __name__ == "__main__":
    # execute only if run as a script
    run_fileformats()
