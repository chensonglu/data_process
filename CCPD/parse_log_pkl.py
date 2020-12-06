import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import numpy as np
import pickle
import math

def forward(x):
    return np.log(20.0*x+1.0)

def inverse(x):
    return (np.exp(x)-1.0)/20.0

model_list = ['carplate_bbox_weights_ssd512_40000.pth',
              'carplate_only_four_corners_weights_ssd512_40000.pth',
              'carplate_bbox_four_corners_weights_ssd512_35000.pth',
              'carplate_bbox_four_corners_with_CIoU_loss_weights_16_ssd512_50000.pth',
              'carplate_only_four_corners_with_CIoU_loss_weights_16_ssd512_50000.pth']
model_list_2 = ['carplate_bbox_weights_ssd512_40000.pth',
                'carplate_only_four_corners_weights_ssd512_40000.pth',
                'carplate_only_four_corners_with_CIoU_loss_weights_16_ssd512_50000.pth']
model_list_4 = ['carplate_bbox_four_corners_weights_ssd512_35000.pth',
                'carplate_bbox_four_corners_with_CIoU_loss_weights_16_ssd512_50000.pth']
set_list = ['ccpd_all_test', 'ccpd_db', 'ccpd_blur', 'ccpd_fn', 'ccpd_rotate',  'ccpd_tilt', 'ccpd_challenge']
set_show_list = ['All', 'DB', 'Blur', 'FN', 'Rotate', 'Tilt', 'Challenge']
IoU_thres_list = [0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
log_root = '/code/ssd.pytorch/log/CCPD_6set_allset_coco'

log_files = os.listdir(log_root)
model_dic = {}
for model_idx, model in enumerate(model_list):
    set_dic = {}
    for log_file in log_files:
        fi = open(os.path.join(log_root, log_file))
        lines = fi.readlines()
        fi.close()

        num_dic = {}
        test_set = lines[0].strip().split('-')[-1]
        coco_ap = 0.0 if lines[1].strip().split(' ')[-1] == 'nan' else float(lines[1].strip().split(' ')[-1])
        num_dic['coco'] = coco_ap
    
        if model in model_list_2 and model in lines[0]:
            F1_score = []
            for i in range(2, 12):
                F1_score.append(0.0 if lines[i].strip().split(' ')[-1] == 'nan' else float(lines[i].strip().split(' ')[-1]))
            num_dic['F1_score'] = F1_score
            num_dic['avg_F1'] = np.mean(np.array(F1_score))
            set_dic[test_set] = num_dic
        elif  model in model_list_4 and model in lines[0]:
            F1_score = []
            for i in range(3, 13):
                F1_score.append(0.0 if lines[i].strip().split(' ')[-1] == 'nan' else float(lines[i].strip().split(' ')[-1]))
            num_dic['F1_score'] = F1_score
            num_dic['avg_F1'] = np.mean(np.array(F1_score))
            set_dic[test_set] = num_dic
    model_dic[model] = set_dic
# print(model_dic)

# ax.set_yscale('function', functions=(forward, inverse))
plt.figure(figsize=(21, 3))
for idx, test_set in enumerate(set_list):
    ax = plt.subplot(1, 7, idx+1)
    ax.set_xscale('logit')
    # ax.set_yscale('linear')
    ax.set_yscale('function', functions=(forward, inverse))
    xmajorLocator = MultipleLocator(0.1)
    # xminorLocator = MultipleLocator(0.05)
    xmajorFormatter = FormatStrFormatter('%2.1f')
    # xminorFormatter = FormatStrFormatter('%3.2f')
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.xaxis.set_major_formatter(xmajorFormatter)
    ax.xaxis.set_minor_locator(plt.NullLocator())
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
    ax.yaxis.set_minor_locator(plt.NullLocator())
    ax.yaxis.set_minor_formatter(plt.NullFormatter())
    for i, model in enumerate(model_list):
        color = plt.rcParams['axes.prop_cycle'].by_key()['color'][i-1]
        F1_score = np.array(model_dic[model][test_set]['F1_score'])[:]
        ax.plot(np.array(IoU_thres_list)[:], F1_score, 'o-', linewidth=1, ms=2, color=color)
    plt.grid(linestyle='--')
    plt.xlabel('IoU')
    if idx == 0:
        plt.ylabel('F1-score')
    plt.title(set_show_list[idx])
    if idx == 0:
        ax.legend(['BB', 'FC', 'BB+FC', 'BB+FC+CIoU', 'FC+CIoU'], handletextpad=0.5, labelspacing=0.3, fontsize=9)
plt.tight_layout()
# plt.subplots_adjust(hspace=0)
# plt.margins(0, 0)
plt.savefig('/home/yzbj/F1.pdf', bbox_inches='tight')
plt.show()


pkl_root = '/code/ssd.pytorch/eval/ssd_carplate_bbox_or_four_corners/test/CCPD_6set_allset_coco'
pkl_files = os.listdir(pkl_root)
model_dic = {}
for model_idx, model in enumerate(model_list):
    set_dic = {}
    for set_idx, test_set in enumerate(set_list):
        for pkl_file in pkl_files:
            if model in pkl_file and test_set in pkl_file:
                with open(os.path.join(pkl_root, pkl_file), 'rb') as f:
                    try:
                        ours_recs = pickle.load(f)
                    except:
                        ours_recs = pickle.load(f, encoding='bytes')

                num_dic = {}
                ap = []
                for idx, kv in enumerate(ours_recs['metrics'].items()):
                    if idx < 10:
                        ap.append(kv[1][0]['ap'])
                    else:
                        num_dic['map'] = kv[1]
                num_dic['ap'] = ap
                set_dic[test_set] = num_dic
                    
    model_dic[model] = set_dic

plt.figure(figsize=(21, 3))
for idx, test_set in enumerate(set_list):
    ax = plt.subplot(1, 7, idx+1)
    ax.set_xscale('logit')
    ax.set_yscale('log')
    xmajorLocator = MultipleLocator(0.1)
    xmajorFormatter = FormatStrFormatter('%2.1f')
    ax.xaxis.set_major_locator(xmajorLocator)
    ax.xaxis.set_major_formatter(xmajorFormatter)
    ax.xaxis.set_minor_locator(plt.NullLocator())
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
    ymajorLocator = MultipleLocator(0.1)
    ymajorFormatter = FormatStrFormatter('%2.1f')
    ax.yaxis.set_major_locator(ymajorLocator)
    ax.yaxis.set_major_formatter(ymajorFormatter)
    ax.xaxis.set_minor_locator(plt.NullLocator())
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
    ax.yaxis.set_minor_locator(plt.NullLocator())
    ax.yaxis.set_minor_formatter(plt.NullFormatter())
    ax.set_yticks([0.1, 0.2, 0.3, 0.5, 1.0])
    for i, model in enumerate(model_list):
        color = plt.rcParams['axes.prop_cycle'].by_key()['color'][i-1]
        F1_score = np.array(model_dic[model][test_set]['ap'])[:]
        ax.plot(np.array(IoU_thres_list)[:], F1_score, 'o-', linewidth=1, ms=2, color=color)
    plt.grid(linestyle='--')
    plt.xlabel('IoU')
    if idx == 0:
        plt.ylabel('AP')
    plt.title(set_show_list[idx])
    if idx == 0:
        ax.legend(['BB', 'FC', 'BB+FC', 'BB+FC+CIoU', 'FC+CIoU'], handletextpad=0.5, labelspacing=0.3, fontsize=9)
plt.tight_layout()
# plt.subplots_adjust(hspace=0)
# plt.margins(0, 0)
plt.savefig('/home/yzbj/AP.pdf', bbox_inches='tight')
plt.show()

