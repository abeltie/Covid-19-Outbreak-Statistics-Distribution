import time
import json
import requests
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.figure
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.rcParams['font.sans-serif'] = ['FangSong']
plt.rcParams['axes.unicode_minus'] = False


def catch_daily():
	url = 'https://view.inews.qq.com/g2/getOnsInfo?name=wuwei_ww_cn_day_counts&callback=&_=%d' % int(time.time() * 1000)
	data = json.loads(requests.get(url=url).json()['data'])
	data.sort(key=lambda x: x['date'])
	date_list = list()
	confirm_list = list()
	suspect_list = list()
	dead_list = list()
	heal_list = list()
	for item in data:
		month, day = item['date'].split('/')
		date_list.append(datetime.strptime('2020-%s-%s' % (month, day), '%Y-%m-%d'))
		confirm_list.append(int(item['confirm']))
		suspect_list.append(int(item['suspect']))
		dead_list.append(int(item['dead']))
		heal_list.append(int(item['heal']))
	return date_list, confirm_list, suspect_list, dead_list, heal_list


def catch_distribution():
	data = {}
	for item in data:
		if item['province'] not in data:
			data.update({item['province']: 0})
			data[item['province']] += int(item['total_confirm'])
	return data


def plot_daily():
	date_list, confirm_list, suspect_list, dead_list, heal_list = catch_daily()  # 获取数据
	plt.figure('2019-nCoV Outbreak Statistics', facecolor='#f4f4f4', figsize=(10, 8))
	plt.title('2019-nCoV Outbreak Curve', fontsize=20)
	plt.plot(date_list, confirm_list, label='确诊')
	plt.plot(date_list, suspect_list, label='疑似')
	plt.plot(date_list, dead_list, label='死亡')
	plt.plot(date_list, heal_list, label='治愈')
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))  # 格式化时间轴标注
	plt.gcf().autofmt_xdate()  # 优化标注（自动倾斜）
	plt.grid(linestyle=':')  # 显示网格
	plt.legend(loc='best')  # 显示图例
	plt.savefig('2019-nCoV Outbreak Curve.png')  # 保存为文件
	plt.show()


def plot_distribution():
	data = catch_distribution()
	font = FontProperties(
		fname='C:/Users/Abel Tie/PycharmProjects/Wuhan Virus Outbreak/venv/Lib/site-packages/china-shapefiles/simsun.ttf',
		size=14
	)
	lat_min = 0
	lat_max = 60
	lon_min = 70
	lon_max = 140
	handles = [
		matplotlib.patches.Patch(color='#ffaa85', alpha=1, linewidth=0),
		matplotlib.patches.Patch(color='#ff7b69', alpha=1, linewidth=0),
		matplotlib.patches.Patch(color='#bf2121', alpha=1, linewidth=0),
		matplotlib.patches.Patch(color='#7f1818', alpha=1, linewidth=0),
	]
	labels = ['1-9 ppl', '10-99 ppl', '100-999 ppl', '>1000 ppl']
	fig = matplotlib.figure.Figure()
	fig.set_size_inches(10, 8)  # 设置绘图板尺寸
	axes = fig.add_axes((0.1, 0.12, 0.8, 0.8))  # rect = l,b,w,h
	m = Basemap(llcrnrlon=lon_min, urcrnrlon=lon_max, llcrnrlat=lat_min, urcrnrlat=lat_max, resolution='l', ax=axes)
	m = Basemap(projection='ortho', lat_0=30, lon_0=105, resolution='l', ax=axes)
	m = Basemap(projection='ortho', lat_0=30, lon_0=105, resolution='l', ax=axes)
	m.readshapefile(
		'C:/Users/Abel Tie/PycharmProjects/Wuhan Virus Outbreak/venv/Lib/site-packages/china-shapefiles/china',
		'province', drawbounds=True)
	m.readshapefile(
		'C:/Users/Abel Tie/PycharmProjects/Wuhan Virus '
		'Outbreak/venv/Lib/site-packages/china-shapefiles/china_nine_dotted_line',
		'section', drawbounds=True)
	m.drawcoastlines(color='black')  # 洲际线
	m.drawcountries(color='black')  # 国界线
	# m.drawparallels(np.arange(lat_min, lat_max, 10), labels=[1, 0, 0, 0])  # 画经度线
	# m.drawmeridians(np.arange(lon_min, lon_max, 10), labels=[0, 0, 0, 1])  # 画纬度线

	for info, shape in zip(m.province_info, m.province):
		pname = info['OWNER'].strip('\x00')
		fcname = info['FCNAME'].strip('\x00')
		if pname != fcname:  # 不绘制海岛
			continue

		for key in data.keys():
			if key in pname:
				if data[key] == 0:
					color = '#f0f0f0'
					poly = Polygon(shape, facecolor=color, edgecolor=color)
					axes.add_patch(poly)
				elif data[key] < 10:
					color = '#ffaa85'
					poly = Polygon(shape, facecolor=color, edgecolor=color)
					axes.add_patch(poly)
				elif data[key] < 100:
					color = '#ff7b69'
					poly = Polygon(shape, facecolor=color, edgecolor=color)
					axes.add_patch(poly)
				elif data[key] < 1000:
					color = '#bf2121'
					poly = Polygon(shape, facecolor=color, edgecolor=color)
					axes.add_patch(poly)
				else:
					color = '#7f1818'
					poly = Polygon(shape, facecolor=color, edgecolor=color)
					axes.add_patch(poly)
				break

	axes.legend(handles, labels, bbox_to_anchor=(0.5, -0.11), loc='lower center', ncol=4, prop=font)
	axes.set_title("2019-nCoV Outbreak Distribution", fontproperties=font)
	FigureCanvasAgg(fig)
	fig.savefig('2019-nCoV Outbreak Distribution.png')
	fig.set_visible(b=True)


if __name__ == '__main__':
	plot_daily()
	plot_distribution()

"""lis = []
		for m in range(len(data['areaTree'][0]['children'])):
			for n in range(len(data['areaTree'][0]['children'][m]['children'])):
				info = {}
				info['country'] = data['areaTree'][0]['name']
				info['province'] = data['areaTree'][0]['children'][m]['name']
				info['city'] = data['areaTree'][0]['children'][m]['children'][n]['name']
				info['total_confirm'] = data['areaTree'][0]['children'][m]['children'][n]['total']['confirm']
				info['total_suspect'] = data['areaTree'][0]['children'][m]['children'][n]['total']['suspect']
				info['total_dead'] = data['areaTree'][0]['children'][m]['children'][n]['total']['dead']
				info['total_heal'] = data['areaTree'][0]['children'][m]['children'][n]['total']['heal']
				info['today_confirm'] = data['areaTree'][0]['children'][m]['children'][n]['today']['confirm']
				info['today_suspect'] = data['areaTree'][0]['children'][m]['children'][n]['today']['suspect']
				info['today_dead'] = data['areaTree'][0]['children'][m]['children'][n]['today']['dead']
				info['today_heal'] = data['areaTree'][0]['children'][m]['children'][n]['today']['heal']
				lis.append(info)"""