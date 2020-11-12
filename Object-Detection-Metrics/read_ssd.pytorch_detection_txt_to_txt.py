import os

root_file = '/data/TILT/1080p/carplate_only/results/det_test_carplate.txt'
target_dir = '/data/TILT/1080p/carplate_only/detections'

fi = open(root_file)
lines = fi.readlines()
fi.close()
for line in lines:
    img, conf, xmin, ymin, xmax, ymax = line.strip().split(' ')
    fo = open(os.path.join(target_dir, img+'.txt'), 'a+')
    fo.write("carplate %s %s %s %s %s\n"%(conf, xmin, ymin, xmax, ymax))
    fo.close()
