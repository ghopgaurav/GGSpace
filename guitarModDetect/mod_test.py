{"nbformat":4,"nbformat_minor":0,"metadata":{"colab":{"provenance":[],"authorship_tag":"ABX9TyP4aOKoif16+N5p9UithUI8"},"kernelspec":{"name":"python3","display_name":"Python 3"},"language_info":{"name":"python"}},"cells":[{"cell_type":"code","execution_count":null,"metadata":{"id":"rbzoQiq2tEZL"},"outputs":[],"source":["# TITLE- Modulation Detection in Electric Guitar Signals Using Machine Learning\n","\n","\n","\n","\n","\n","\n","# Import necessary libraries\n","from keras import backend as K\n","import os\n","import time\n","import h5py\n","import sys\n","import numpy as np\n","from keras.optimizers import SGD\n","from keras.utils import np_utils\n","from math import floor\n","import matplotlib.pyplot as plt\n","from your_custom_network import GuitarModulationCNN\n","from utils import save_data, load_dataset, save_dataset, sort_result, predict_label, extract_melgrams\n","\n","# Parameters to set\n","TEST = 1\n","\n","LOAD_MODEL = 0\n","LOAD_WEIGHTS = 1\n","MULTIFRAMES = 1\n","time_elapsed = 0\n","\n","# Guitar Modulation Classes\n","mods = ['Chorus', 'Flanger', 'Phaser', 'Tremolo', 'Vibrato', 'Wah-Wah', 'Distortion', 'Ring Modulator', 'Harmonizer']\n","mods = np.array(mods)\n","\n","# Paths to set\n","model_name = \"example_model\"\n","model_path = \"models_trained/\" + model_name + \"/\"\n","weights_path = \"models_trained/\" + model_name + \"/weights/\"\n","\n","test_songs_list = 'list_example.txt'\n","\n","# Initialize model\n","model = GuitarModulationCNN(weights=None, input_tensor=(1, 96, 1366))\n","\n","model.compile(loss='categorical_crossentropy',\n","              optimizer='adam',\n","              metrics=['accuracy'])\n","\n","if LOAD_WEIGHTS:\n","    model.load_weights(weights_path+'crnn_net_gru_adam_ours_epoch_40.h5')\n","\n","#model.summary()\n","\n","X_test, num_frames_test= extract_melgrams(test_songs_list, MULTIFRAMES, process_all_song=False, num_songs_genre='')\n","\n","num_frames_test = np.array(num_frames_test)\n","\n","t0 = time.time()\n","\n","print('\\n--------- Predicting ---------','\\n')\n","\n","results = np.zeros((X_test.shape[0], mods.shape[0]))\n","predicted_labels_mean = np.zeros((num_frames_test.shape[0], 1))\n","predicted_labels_frames = np.zeros((X_test.shape[0], 1))\n","\n","song_paths = open(test_songs_list, 'r').read().splitlines()\n","\n","previous_numFrames = 0\n","n=0\n","for i in range(0, num_frames_test.shape[0]):\n","    print('Song number' +str(i)+ ': ' + song_paths[i])\n","\n","    num_frames=num_frames_test[i]\n","    print('Num_frames of 30s: ', str(num_frames),'\\n')\n","\n","    results[previous_numFrames:previous_numFrames+num_frames] = model.predict(\n","        X_test[previous_numFrames:previous_numFrames+num_frames, :, :, :])\n","\n","    s_counter = 0\n","    for j in range(previous_numFrames, previous_numFrames+num_frames):\n","        #normalize the results\n","        total = results[j,:].sum()\n","        results[j,:]=results[j,:]/total\n","        print('Percentage of modulation prediction for seconds '+ str(20+s_counter*30) + ' to '\n","            + str(20+(s_counter+1)*30) + ': ')\n","        sort_result(mods, results[j,:].tolist())\n","\n","        predicted_label_frames=predict_label(results[j,:])\n","        predicted_labels_frames[n]=predicted_label_frames\n","        s_counter += 1\n","        n+=1\n","\n","    print('\\n', 'Mean modulation of the guitar: ')\n","    results_song = results[previous_numFrames:previous_numFrames+num_frames]\n","\n","    mean=results_song.mean(0)\n","    sort_result(mods, mean.tolist())\n","\n","    predicted_label_mean=predict_label(mean)\n","\n","    predicted_labels_mean[i]=predicted_label_mean\n","    print('\\n','The predicted guitar modulation for the song is', str(mods[predicted_label_mean]),'!\\n')\n","\n","    previous_numFrames = previous_numFrames+num_frames\n","\n","    print('************************************************************************************************')\n","\n","colors = ['b','g','c','r','m','k','y','#ff1122','#5511ff','#44ff22']\n","fig, ax = plt.subplots()\n","index = np.arange(mods.shape[0])\n","opacity = 1\n","bar_width = 0.2\n","print(mean)\n","plt.bar(index, mean, width=bar_width, alpha=opacity, color=colors)\n","\n","plt.xlabel('Modulations')\n","plt.ylabel('Percentage')\n","plt.title('Scores by modulation')\n","plt.xticks(index + bar_width / 2, mods)\n","plt.tight_layout()\n","fig.autofmt_xdate()\n","plt.savefig('modulations_prediction.png')\n","\n","\n"]},{"cell_type":"code","source":["from google.colab import drive\n","drive.mount('/content/drive')\n"],"metadata":{"colab":{"base_uri":"https://localhost:8080/"},"id":"xPT968Z6eFrf","executionInfo":{"status":"ok","timestamp":1698415860877,"user_tz":-330,"elapsed":44195,"user":{"displayName":"Gaurav Ghop","userId":"17071669418159100136"}},"outputId":"3b12cfd7-86ed-4d5a-f9c2-6a27b2c61572"},"execution_count":1,"outputs":[{"output_type":"stream","name":"stdout","text":["Mounted at /content/drive\n"]}]}]}