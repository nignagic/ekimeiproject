from django.db import models

# Create your models here.
class Country(models.Model):
	name = models.CharField('国名', max_length=200)
	def __str__(self):
		return self.name

class Region(models.Model):
	name = models.CharField('地方名', max_length=200)
	country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='国')
	def __str__(self):
		return self.name

class Prefecture(models.Model):
	name = models.CharField('都道府県名', max_length=200)
	region = models.ForeignKey(Region, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='地方')
	def __str__(self):
		return self.name

class CompanyCategory(models.Model):
	name = models.CharField('事業者区分', max_length=200)
	def __str__(self):
		return self.name

class Company(models.Model):
	name = models.CharField('事業者名', max_length=200, null=True, blank=True)
	short_name = models.CharField('略称1', max_length=200, null=True, blank=True)
	short_name_2 = models.CharField('略称2', max_length=200, null=True, blank=True)
	name_kana = models.CharField('事業者名読み', max_length=200, null=True, blank=True)
	color = models.CharField('会社カラー', max_length=100, null=True, blank=True)
	category = models.ForeignKey(CompanyCategory, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='事業者区分')
	sort_by_category = models.IntegerField('区分ごとの並び順', default=0)

	other_option = models.BooleanField('その他の選択肢', default=False)
	def __str__(self):
		return self.name

	def short_text(self):
		if self.short_name_2:
			return self.short_name_2
		elif self.short_name:
			return self.short_name
		elif self.name:
			return name
		else:
			return ""

class BelongsCategory(models.Model):
	name = models.CharField('所属カテゴリー', max_length=100)
	object_name = models.CharField('名称カテゴリー', null=True, blank=True, max_length=100)
	icon = models.CharField('FontAweSomeアイコン名称', null=True, blank=True, max_length=100)
	def __str__(self):
		return self.name

class Line(models.Model):
	category = models.ForeignKey(BelongsCategory, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属カテゴリー')
	formal_name = models.CharField('路線名(鉄道要覧)', max_length=200, null=True, blank=True)
	name = models.CharField('路線名', max_length=200, null=True, blank=True)
	name_sub = models.CharField('路線区別名', max_length=200, null=True, blank=True)
	company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='事業者')
	sort_by_company = models.IntegerField('事業者ごとの並び順', default=0)
	is_freight = models.CharField('貨物輸送', max_length=200, null=True, blank=True)
	prefs = models.ManyToManyField(Prefecture, blank=True)
	STATUS_CHOICES = (
		(0, '運用中'),
		(1, '運用前'),
		(2, '廃止')
	)
	status = models.IntegerField('状態', null=True, blank=True, choices=STATUS_CHOICES, default=0)
	def start_station(self):
		return Station.objects.filter(line=self.pk).order_by('sort_by_line').first()

	def end_station(self):
		return Station.objects.filter(line=self.pk).order_by('sort_by_line').last()

	def with_sub(self):
		if self.name == None:
			return "untitled"
		if self.name_sub:
			return self.name + "(" + self.name_sub + ")"
		else:
			return self.name

	def status_text(self):
		if self.status == 1:
			return "[未]"
		elif self.status == 2:
			return "[廃]"
		else:
			return ""

	def __str__(self):
		if self.name == None:
			return "untitled"
		if self.company == None:
			return "untitled"

		n = ""
		if self.company.short_text():
			n += self.company.short_text() + " " + self.with_sub()
		else:
			n += self.with_sub()

		if self.status_text():
			return n + self.status_text()
		return n

class Station(models.Model):
	# category = models.ForeignKey(ObjectCategory, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='名称カテゴリー')
	group_station = models.ManyToManyField('self', blank=True)
	group_station_new = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='乗換駅(代表)')
	name = models.CharField('駅名', max_length=200, null=True, blank=True)
	line = models.ForeignKey(Line, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='路線')
	sort_by_line = models.IntegerField('路線ごとの並び順', null=True, blank=True, default=0)
	name_kana = models.CharField('駅名読み', max_length=200, null=True, blank=True)
	pref = models.ForeignKey(Prefecture, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='所在地')
	open_ymd = models.DateField('開業年月日', max_length=200, null=True, blank=True)
	close_ymd = models.DateField('廃止年月日', max_length=200, null=True, blank=True)
	lon = models.CharField('経度', max_length=200, null=True, blank=True)
	lat = models.CharField('緯度', max_length=200, null=True, blank=True)
	STATUS_CHOICES = (
		(0, '運用中'),
		(1, '運用前'),
		(2, '廃止')
	)
	status = models.IntegerField('状態', null=True, blank=True, choices=STATUS_CHOICES, default=0)
	is_representative = models.BooleanField('代表オブジェクト', default=False)
	def get_group_station(self):
		g = self.group_station_new
		if g:
			s = Station.objects.filter(group_station_new=g)
		else:
			s = Station.objects.filter(pk=self.id)
		return s

	def get_group_station_id(self):
		g = self.group_station_new
		if g:
			s = Station.objects.filter(group_station_new=g).first().id
		else:
			s = self.id
		return s

	def get_group_station_lines(self):
		ls = Station.objects.filter(group_station_new=self.group_station_new.id)
		text = ""
		for l in ls:
			text = text + l.line.name + " / "
		return text

	def status_text(self):
		if self.status == 1:
			return "[未]"
		elif self.status == 2:
			return "[廃]"
		else:
			return ""

	def __str__(self):
		return self.name + self.status_text()

class LineService(models.Model):
	category = models.ForeignKey(BelongsCategory, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='所属カテゴリー')
	name = models.CharField('路線名(運行系統名)', max_length=200, null=True, blank=True)
	name_sub = models.CharField('路線区別名', max_length=200, null=True, blank=True, default="")
	line = models.ManyToManyField(Line, blank=True, verbose_name='正式路線')
	head_company_name = models.CharField('接頭会社名', max_length=200, null=True, blank=True, default="")
	company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='事業者')
	sort_by_company = models.IntegerField('事業者ごとの並び順', default=999)
	is_formal = models.CharField('正式区間', max_length=200, null=True, blank=True, default=1)
	is_service = models.CharField('運行系統', max_length=200, null=True, blank=True, default=1)
	color = models.CharField('路線カラー', max_length=100, null=True, blank=True)
	prefs = models.ManyToManyField(Prefecture, blank=True)
	STATUS_CHOICES = (
		(0, '運用中'),
		(1, '運用前'),
		(2, '廃止')
	)
	status = models.IntegerField('状態', null=True, blank=True, choices=STATUS_CHOICES, default=0)
	def start_station(self):
		return StationService.objects.filter(line_service=self.pk).order_by('sort_by_line_service').exclude(is_representative=True).first()

	def end_station(self):
		return StationService.objects.filter(line_service=self.pk).order_by('sort_by_line_service').exclude(is_representative=True).last()

	def f_or_s(self):
		a = self.is_formal
		b = self.is_service
		if self.is_formal and (self.is_service=="" or self.is_service is None):
			return "[正式区間]"
		elif (self.is_formal=="" or self.is_formal is None) and self.is_service:
			return "[運行系統]"
		else:
			return ""

	def with_sub(self):
		if self.name == None:
			return "untitled"
		if self.name_sub:
			return self.name + "(" + self.name_sub + ")"
		else:
			return self.name

	def status_text(self):
		if self.status == 1:
			return "[未]"
		elif self.status == 2:
			return "[廃]"
		else:
			return ""

	def __str__(self):
		if self.name == None:
			return "untitled"
		if self.company == None:
			return "untitled"

		n = ""
		if self.company.short_text():
			n += self.company.short_text() + " " + self.with_sub()
		else:
			n += self.with_sub()

		if self.f_or_s():
			return n + self.f_or_s()

		if self.status_text():
			return n + self.status_text()
		return n

class StationService(models.Model):
	# category = models.ForeignKey(ObjectCategory, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='名称カテゴリー')
	name = models.CharField('駅名(運行系統)', max_length=200, null=True, blank=True)
	station = models.ForeignKey(Station, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='駅(正式)')
	group_station_service = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='駅グループコード[運行系統]')
	# group_station_service: 山手線の東京駅など、正式区間を横断する運行系統を接続する駅をまとめる
	line_service = models.ForeignKey(LineService, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='路線(運行系統)')
	numbering_head = models.CharField('ナンバリング接頭辞', max_length=200, null=True, blank=True, default='')
	numbering_symbol = models.CharField('路線記号', max_length=200, null=True, blank=True, default='')
	numbering_middle = models.CharField('ナンバリングハイフン', max_length=200, null=True, blank=True, default='')
	numbering_number = models.CharField('駅番号', max_length=200, null=True, blank=True, default='')
	sort_by_line_service = models.IntegerField('路線(運行系統)ごとの並び順', null=True, blank=True, default=0)
	color = models.CharField('駅カラー', max_length=100, null=True, blank=True, default='')
	is_representative = models.BooleanField('代表オブジェクト', default=False)
	def prev_station_base(self):
		# 路線上の純粋な並び替えで前の駅オブジェクトを取得
		return type(self).objects.filter(line_service=self.line_service).filter(sort_by_line_service__lt=self.sort_by_line_service).order_by('sort_by_line_service').last()

	def next_station_base(self):
		# 路線上の純粋な並び替えで後の駅オブジェクトを取得
		return type(self).objects.filter(line_service=self.line_service).filter(sort_by_line_service__gt=self.sort_by_line_service).order_by('sort_by_line_service').first()

	def get_group_station_service(self):
		g = self.group_station_service
		if g:
			s = StationService.objects.filter(group_station_service=g).exclude(pk=self.id).first()
		else:
			s = None
		return s

	def prev_group(self):
		p = self.prev_station_base()
		if p and (self.get_group_station_service() == p):
			return p
		else:
			return self

	def next_group(self):
		n = self.next_station_base()
		if n and (self.get_group_station_service() == n):
			return n
		else:
			return self

	def prev_station(self):
		p = self.prev_station_base()
		if p:
			if self.station.get_group_station().filter(pk=p.station.id):
				p = p.prev_station_base()
		return p

	def next_station(self):
		n = self.next_station_base()
		if n:
			if self.station.get_group_station().filter(pk=n.station.id):
				n = n.next_station_base()
		return n

	def get_pref(self):
		if self.station:
			if self.station.pref:
				return self.station.pref.name
			else:
				return ""
		else:
			return ""

	def get_numbering(self):
		if self.numbering_middle == "space":
			mid = " "
		elif self.numbering_middle:
			mid = self.numbering_middle
		else:
			mid = ""
		if self.numbering_head:
			h = self.numbering_head
		else:
			h = ""
		if self.numbering_symbol:
			s = self.numbering_symbol
		else:
			s = ""
		if self.numbering_number:
			n = self.numbering_number
		else:
			n = ""
		return h + s + mid + n

	def get_color(self):
		s = self.color
		if self.line_service:
			l = self.line_service.color
		else:
			l = ""
		if self.line_service.company:
			c = self.line_service.company.color
		else:
			c = ""
			
		if s != "" and s != None:
			return s
		elif l != "" and l != None:
			return l
		elif c != "" and c != None:
			return c
		else:
			return "#06262b"

	def status_text(self):
		if self.station.status == 1:
			return "[未]"
		elif self.station.status == 2:
			return "[廃]"
		else:
			return ""

	def __str__(self):
		return self.name + self.status_text()

class StationServiceHistory(models.Model):
	# category_history = models.ForeignKey(ObjectCategory, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='名称カテゴリー')
	name_history = models.CharField('駅名(運行系統)', max_length=200, null=True, blank=True)
	station_history = models.ForeignKey(Station, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='駅(正式)')
	line_service_history = models.ForeignKey(LineService, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='路線(運行系統)')
	numbering_head_history = models.CharField('ナンバリング接頭辞', max_length=200, null=True, blank=True, default='')
	numbering_symbol_history = models.CharField('路線記号', max_length=200, null=True, blank=True, default='')
	numbering_middle_history = models.CharField('ナンバリングハイフン', max_length=200, null=True, blank=True, default='')
	numbering_number_history = models.CharField('駅番号', max_length=200, null=True, blank=True, default='')
	sort_by_line_service_history = models.IntegerField('路線(運行系統)ごとの並び順', null=True, blank=True, default=0)
	color_history = models.CharField('駅カラー', max_length=100, null=True, blank=True, default='')
	changed_date = models.DateField('変更年月日', max_length=200, null=True, blank=True)

	def __str__(self):
		return self.name_history

class ErrorList(models.Model):
	category = models.CharField('種類', max_length=200)
	text = models.TextField('内容', max_length=500)

	def __str__(self):
		return self.text