import os
import pickle

pkl_root = '/code/ssd.pytorch/eval/ssd_carplate_bbox_or_four_corners/test/'
pkl_file = 'carplate-CCPD_carplate_bbox_with_CIoU_loss_weights_16_ssd300_55000.pth-ccpd_all_test-bbox-coco-pr.pkl'

with open(os.path.join(pkl_root, pkl_file), 'rb') as f:
    try:
        ours_recs = pickle.load(f)
    except:
        ours_recs = pickle.load(f, encoding='bytes')

print(ours_recs)
