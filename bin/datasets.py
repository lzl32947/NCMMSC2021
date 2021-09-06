import json

import numpy as np
from torch.utils.data.dataloader import DataLoader

from configs.types import AudioFeatures, DatasetMode
from util.train_util.data_loader import AldsDataset2D, AldsDataset1D
from util.tools.files_util import global_init
import time
import matplotlib.pyplot as plt

from util.log_util.logger import GlobalLogger
from util.train_util.trainer_util import prepare_feature, prepare_dataloader


def test_dataset1D():
    """
    This file is used to test the datasets(dataloader), and be stored in directory 'bin'
    """
    # Get the global identifier and the configs
    time_identifier, configs = global_init("config_audio")
    # Get the logger
    logger = GlobalLogger().get_logger()
    # Init the features to use
    use_features = prepare_feature(configs['features'])

    # Get the dataloader from the generator
    for dataloader in prepare_dataloader(use_features, AldsDataset1D, configs["dataset"], DatasetMode.TRAIN, k_fold=0):
        logger.info("Using config:" + json.dumps(configs['dataset']['process'], ensure_ascii=False))
        # Calculate the process time
        now_time = time.time()
        for item in dataloader:
            # Restore the batch to (Batch, E, Length)
            item = np.transpose(item, [1, 0, 2])
            # Store the time of processing
            current_time = time.time()
            # Write log
            logging_str = ""
            for index, features in enumerate(use_features):
                logging_str = logging_str + ("{}->{}\t".format(use_features[index].value, item[features].shape))
            logging_str = logging_str + "label: {}\t".format(item[AudioFeatures.LABEL])
            logging_str = logging_str + "time use: {:<.2f}".format(current_time - now_time)
            logger.info(logging_str)
            # Get the batch
            batch_size = item[AudioFeatures.LABEL].shape[0]
            for batch_num in range(batch_size):
                # Plot the data in each figure
                fig = plt.figure()
                plot_position = 1
                for index, features in enumerate(item.keys()):
                    # Ignore the label
                    if features == AudioFeatures.LABEL:
                        continue

                    # Add the subplot to figure
                    ax = fig.add_subplot(len(item.keys()) - 1, 1, plot_position)
                    plot_position += 1

                    # If in format of Mat(2 dimension) then use the matshow()
                    if len(item[features][batch_num].shape) == 2:
                        ax.matshow(item[features][batch_num],aspect='auto')
                    # In format of Image(3 dimension) and use the imshow()
                    elif len(item[features][batch_num].shape) == 3:
                        img = np.transpose(item[features][batch_num], (1, 2, 0))
                        ax.imshow(img,aspect='auto')
                    # In format of Audio(1 dimension) and use the plot()
                    elif len(item[features][batch_num].shape) == 1:
                        ax.plot(range(len(item[features][batch_num])), item[features][batch_num])
                    # Add the title
                    ax.set_title("{}".format(list(item.keys())[index].value))
                # Plot the image
                plt.tight_layout()
                fig.show()
                plt.close(fig)
            # Update the time
            now_time = time.time()


def test_dataset2D():
    """
    This file is used to test the datasets(dataloader), and be stored in directory 'bin'
    """
    # Get the global identifier and the configs
    time_identifier, configs = global_init("config")
    # Get the logger
    logger = GlobalLogger().get_logger()
    # Init the features to use
    use_features = prepare_feature(configs['features'])

    # Get the dataloader from the generator
    for dataloader in prepare_dataloader(use_features, AldsDataset2D, configs["dataset"], DatasetMode.TRAIN, k_fold=0):
        logger.info("Using config:" + json.dumps(configs['dataset']['process'], ensure_ascii=False))
        # Calculate the process time
        now_time = time.time()
        for item in dataloader:
            # Store the time of processing
            current_time = time.time()
            # Write log
            logging_str = ""
            for index, features in enumerate(use_features):
                logging_str = logging_str + ("{}->{}\t".format(use_features[index].value, item[index].shape))
            logging_str = logging_str + "label: {}\t".format(item[-1])
            logging_str = logging_str + "time use: {:<.2f}".format(current_time - now_time)
            logger.info(logging_str)
            # Get the batch
            batch_size = item[0].shape[0]
            for batch_num in range(batch_size):
                # Plot the data in each figure
                fig = plt.figure()
                plot_position = 1
                for index, features in enumerate(use_features):
                    # Add the subplot to figure
                    ax = fig.add_subplot(len(use_features), 1, plot_position)
                    plot_position += 1
                    # If in format of Mat(2 dimension) then use the matshow()
                    if len(item[index][batch_num].shape) == 2:
                        ax.matshow(item[index][batch_num])
                    # In format of Image(3 dimension) and use the imshow()
                    else:
                        img = np.transpose(item[index][batch_num], (1, 2, 0))
                        ax.imshow(img)
                    # Add the title
                    ax.set_title("{}".format(use_features[index].value))
                # Plot the image
                plt.tight_layout()
                fig.show()
                plt.close(fig)
            # Update the time
            now_time = time.time()


if __name__ == '__main__':
    test_dataset1D()
