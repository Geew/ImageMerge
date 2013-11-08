# coding: utf8
from PIL import Image, ImageDraw
import datetime
import os.path


class MergeImage(object):

    _max_count = 9
    _merge_image_size = (640, 640)
    _gap = 5

    def __init__(self, images, save_name=''):
        self.images = images[:self._max_count]
        self.blocks = len(self.images) + len(self.images) % 2
        if self.blocks > self._max_count:
            self.blocks = self._max_count
        self.col = 2 if self.blocks < self._max_count else 3
        self.row = self.blocks / self.col
        path = os.path.split(self.images[0])[0]
        if not save_name:
            self.save_name = os.path.join(path, 'merge' + datetime.datetime.now().strftime('%y%m%d-%s') + '.png')
        else:
            self.save_name = os.path.join(path, save_name)

    def draw_line(self, img):
        """ 画一些分割线
        """
        return img

    def get_size(self):
        """ 获取缩略图的大小
        """
        max_hei = self._merge_image_size[1] / self.col
        max_wid = self._merge_image_size[0] / self.row
        return max_wid, max_hei

    def get_thumbnails(self):
        """ 获取调整的缩略图
        """
        size = list(self.get_size())
        size[0] = size[0] - self._gap
        thumbnails = []
        for i in self.images:
            img = Image.open(i)
            img.thumbnail(tuple(size), Image.ANTIALIAS)
            thumbnails.append(img)
        return thumbnails

    def paste(self):
        """ 粘贴
        """
        nimg = Image.new('RGB', self._merge_image_size, 'white')
        nimg = self.draw_line(nimg)
        thumbnails = self.get_thumbnails()
        wid, hei = self.get_size()
        pos = []
        for j in range(self.col):
            for i in range(self.row):
                pos.append((int((0.5+i)*wid), int((0.5+j)*hei)))
        self.pos = pos
        for i, img in enumerate(thumbnails):
            iwid, ihei = img.size
            p = (pos[i][0] - int(iwid/2), pos[i][1] - int(ihei/2))
            nimg.paste(img, p)
        return nimg

    def save(self):
        """ 保存
        """
        nimg = self.paste()
        nimg.save(self.save_name)
