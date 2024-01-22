/* modified in 2022/11/06 */

//YouTubeジャンプ
$('.youtube-jump').on('click', function() {
	time = $(this).siblings('.start_time').val()
	player.playVideo();
	player.seekTo(TimetoSecond(time), true);
})

function TimetoSecond(time) {
	t = time.split(':');
	hour = parseInt(t[0]) * 3600;
	minute = parseInt(t[1]) * 60;
	second = parseInt(t[2]);
	return hour + minute + second;
}

$(function() {
	d = $('.movie-description').text().replace(/<br>/g, '<br>');
	$('.movie-description').html(d)

	// ページ読み込み時の、参加者情報読み込み
	ps = $('#selected_participant_list .selected_participant');
	selected_participant_list = ""
	ps.each(function (i, val) {
		if (i != 0) selected_participant_list += ","
		selected_participant_list += val.value
	})
	add_selected_participant(selected_participant_list)

	// ページ読み込み時の、楽曲情報読み込み
	ss = $('#selected_song_in_part_list .selected_song_in_part');
	selected_song_in_part_list = ""
	ss.each(function (i, val) {
		if (i != 0) selected_song_in_part_list += ","
		selected_song_in_part_list += val.value
	})
	add_selected_song(selected_song_in_part_list)

	// ページ読み込み時の、ボーカル情報読み込み
	vs = $('#selected_vocal_list .selected_vocalnew');
	selected_vocal_list = ""
	vs.each(function (i, val) {
		if (i != 0) selected_vocal_list += ","
		selected_vocal_list += val.value
	})
	add_selected_vocal(selected_vocal_list)
})

// 参加者変更
function add_selected_participant(list) {
	participants = list.split(',')
	$('#selected_participant_list').empty()
	$('#selected_participant_name').empty();
	if (participants == "") {
		$('#selected_participant_name').append("未設定");
	} else {
		$.each(participants, function(i, val) {
			txt = "<input type='hidden' name='participant' value='" + val + "' class='selected_participant' id='id_participant_" + i + "'>"
			$('#selected_participant_list').append(txt)

			var s = "/api/name/" + val + "?format=json";
			n = ""
			$.getJSON(s, function(data) {
				for (var i in data) {
					$("#selected_participant_name").append("<p>" + data[i].name + "</p>");
				}
			})
		})
	}
}

// 楽曲変更
function add_selected_song(list) {
	songs = list.split(',')
	$('#selected_song_in_part_list').empty()
	$('#selected_song_in_part_name').empty();
	if (songs == "") {
		$('#selected_song_in_part_name').append("未設定");
	} else {
		$.each(songs, function(i, val) {
			txt = "<input type='hidden' name='songnew' value='" + val + "' class='selected_song_in_movie' id='id_songnew_" + i + "'>"
			$('#selected_song_in_part_list').append(txt)

			var s = "/songdata/api/songnew/" + val + "?format=json";
			n = ""
			$.getJSON(s, function(data) {
				for (var i in data) {
					$("#selected_song_in_part_name").append("<p>" + data[i].__str__ + "</p>");
				}
			})
		})
	}
}

// ボーカル変更
function add_selected_vocal(list) {
	vocals = list.split(',')
	$('#selected_vocal_list').empty()
	$('#selected_vocal_name').empty();
	if (vocals == "") {
		$('#selected_vocal_name').append("未設定");
	} else {
		$.each(vocals, function(i, val) {
			txt = "<input type='hidden' name='vocalnew' value='" + val + "' class='selected_vocalnew' id='id_vocalnew_" + i + "'>"
			$('#selected_vocal_list').append(txt)

			var s = "/songdata/api/vocal/" + val + "?format=json";
			n = ""
			$.getJSON(s, function(data) {
				for (var i in data) {
					$("#selected_vocal_name").append("<p>" + data[i].vocal_name + "</p>");
				}
			})
		})
	}
}

// 都道府県を選択したときの挙動
$('#pref-select').children('div').on('click', function() {
	pref = $(this).attr('value');
	var s = "/api/pref/" + pref + "/lineservice/?format=json";
	$(".pref-line-select").empty();
	$.getJSON(s, function(data) {
		for (var i in data) {
			name_sub = data[i].name_sub ? "(" + data[i].name_sub + ")" : "";
			var op_line = "<div value='" + data[i].line_service_pk + "' class='line-option'><span class='linelist-company-name'>" + data[i].company_short_name + "</span>" + data[i].name + "<span>" + name_sub + data[i].status_text + data[i].f_or_s + "</span>" + "</div>";
			$(".pref-line-select").append(op_line);
		}
	})
})

// 事業者名を選択したときの挙動
$('#company-select').children('div').on('click', function() {
	company = $(this).attr('value');
	var s = "/api/company/" + company + "/lineservice/?format=json";
	$(".company-line-select").empty();
	$.getJSON(s, function(data) {
		for (var i in data) {
			name_sub = data[i].name_sub ? "(" + data[i].name_sub + ")" : "";
			var op_line = "<div value='" + data[i].line_service_pk + "' class='line-option'>" + data[i].name + "<span>" + name_sub + data[i].status_text + data[i].f_or_s + "</span>" + "</div>";
			$(".company-line-select").append(op_line);
		}
	})
})

//路線を選択した時の挙動
$(document).on('click', '.line-option', function() {
	line = $(this).attr("value");
	var s = "/api/lineservice/" + line + "/stationservice/?format=json";
	$('.station-select').empty();
	$.getJSON(s, function(data) {
		for (var i in data) {
			pk = data[i].station_service_pk
			str = data[i].__str__
			name = data[i].name
			get_group_station = data[i].get_group_station
			line_service_pk = data[i].line_service_pk
			category = data[i].category
			pref = data[i].pref
			get_color = data[i].get_color
			is_representative = data[i].is_representative
			other_option = data[i].other_option
			status_text = data[i].status_text
			line_service_name = data[i].line_service_name

			var op_station = "<option value='" + pk + "' data-name='" + name + "' data-get_group_station='" + get_group_station + "' data-line_service_pk='" + line_service_pk + "' data-category='" + category + "' data-pref='" + pref + "' data-get_color='" + get_color + "' data-is_representative='" + is_representative + "' data-other_option='" + other_option + "' data-status='" + status_text + "' data-line='" + line_service_name + "' class='station-option'>" + str +  "</option>"
			$(".station-select").append(op_station);
		}
	})
})

//逆順にした時の挙動
$(document).on('click', '.station-reverse', function() {
	var list = $('.station-option').toArray().reverse();
	$('.station-select').empty().append(list);
})

//乗換検索をした時の挙動
$(document).on('click', '.station-line-search-button', function() {
	station = $(this).parents('.station-box').find('.station_service').attr("value");
	var s = "/api/transfer/" + station + "/?format=json";
	$(".transfer-line-select").empty();

	$('.is-active').removeClass('is-active');
	$('.tab-transfer').addClass('is-active');
	$('.is-show').removeClass('is-show');
	const index = $('.tab-transfer').index();
	$('.tab-content').eq(index).addClass('is-show');

	$.getJSON(s, function(data) {
		for (var i in data) {
			var op_line = "<div value='" + data[i].line_service_pk + "' class='line-option'>" + data[i].__str__ + "</div>";
			$(".transfer-line-select").append(op_line);
		}
	})
})

//タブを切り替えた時の挙動
$(function() {
	$('.tab').click(function() {
		$('.station-select').empty();

		$('.is-active').removeClass('is-active');
		$(this).addClass('is-active');

		$('.is-show').removeClass('is-show');
		const index = $(this).index();
		$('.tab-content').eq(index).addClass('is-show');

		$('.is-queue-show').removeClass('is-queue-show');
		if ($(this).hasClass('tab-other')) {
			$('.station-name-input-container').addClass('is-queue-show')
		} else {
			$('.station-queue').addClass('is-queue-show')
		}
	})
})

//駅名検索をした時の挙動
$('.namesearch').keypress(function(e) {
	if (e.which == 13) {
		namesearch();
	}
})
$('.namesearchbutton').on('click', function() {
	namesearch();
})
function namesearch() {
	text = $('.namesearch').val();
	var s = "/api/stationsearch/" + text + "/?format=json";
	$('.station-select').empty();
	$.getJSON(s, function(data) {
		for (var i in data) {
			pk = data[i].station_service_pk
			str = data[i].__str__
			name = data[i].name
			get_group_station = data[i].get_group_station
			line_service_pk = data[i].line_service_pk
			category = data[i].category
			pref = data[i].pref
			get_color = data[i].get_color
			is_representative = data[i].is_representative
			other_option = data[i].other_option
			status_text = data[i].status_text

			company_short_name = data[i].company_short_name
			line_service_name = data[i].line_service_name
			f_or_s = data[i].line_service_f_or_s
			line_name = data[i].line_name
			text = ""
			if (line_service_name != line_name) {
				text = str + " ‐ " + company_short_name + " " + line_service_name + f_or_s + "(" + line_name + ")"
			} else {
				text = str + " ‐ " + company_short_name + " " + line_service_name + f_or_s
			}
			op_station = "<option value='" + pk + "' data-name='" + name + "' data-get_group_station='" + get_group_station + "' data-line_service_pk='" + line_service_pk + "' data-category='" + category + "' data-pref='" + pref + "' data-get_color='" + get_color + "' data-is_representative='" + is_representative + "' data-other_option='" + other_option + "' data-status='" + status_text + "' data-line='" + line_service_name + "' class='station-option' title='" + text + "'>" + text +  "</option>"
			$('.station-select').append(op_station)
		}
	})
}

// 廃駅入力エリアの挙動
$(function() {
	const text = `ここに駅名を入力

例）
東京
神田
秋葉原

「追加」ボタンで、この順番にオブジェクトが生成されます。`
	$('#station-name-input').attr('placeholder', text)
})

$(document).ready(function() {
	$('input,textarea[readonly]').not($('input[type="button"],input[type="submit"]')).keypress(function (e) {
		if (!e) var e = window.event;
		if (e.keyCode == 13) return false;
	})
})

//駅登録リスト
$(function() {
	$('.selected-list').html(
		$('.station_form').sort(function(a,b) {
			return parseInt($(a).find('.sort_by_part').val(), 10) - parseInt($(b).find('.sort_by_part').val(), 10)
		})
	)

	$('.sortable-delete input').prop('checked', false)
	$('.sortable-delete input').hide()

	var totalManageElement = $('input#id_stationinmovie-TOTAL_FORMS');
	var currentFileCount = parseInt(totalManageElement.val());
	console.log(currentFileCount)

	$(document).on('click', '.station-append', function() {

		if ($('.is-queue-show').hasClass('station-queue')) {

			$('.station-select option:selected').each(function() {
				station_append(this);
				
			})

		} else {

			option = $('[name=other] option:selected')
			console.log(option)
			names = $('#station-name-input').val().split('\n')
			$.each(names, function(i, val) {
				station_append(option, val)
			})

		}

		$('.station_form').each(function(i, form) {
			$(form).find('.sort_by_part').val(i);
		})
		
		$('.selected-list').animate({scrollTop:$('.selected-list')[0].scrollHeight}, 300);
	})

	$(document).on('dblclick', '.station-option', function() {
		station_append(this)

		$('.station_form').each(function(i, form) {
			$(form).find('.sort_by_part').val(i);
		})
		
		$('.selected-list').animate({scrollTop:$('.selected-list')[0].scrollHeight}, 300);
	})

	// その他オプションの選択
	$(document).on('dblclick', '.other-option', function() {
		station_append(this)

		$('.station_form').each(function(i, form) {
			$(form).find('.sort_by_part').val(i);
		})
		
		$('.selected-list').animate({scrollTop:$('.selected-list')[0].scrollHeight}, 300);
	})

	function station_append(station, sung_name) {
		val = $(station).attr("value");
		station_name = $(station).data('name');
		if (!sung_name) sung_name = station_name

		get_group_station = $(station).data('get_group_station');
		line_service_pk = $(station).data('line_service_pk');
		category = $(station).data('category');
		pref = $(station).data('pref');
		get_color = $(station).data('get_color');
		is_representative = $(station).data('is_representative');
		other_option = $(station).data('other_option');

		status_text = $(station).data('status');
		line_name = $(station).data('line');

		var element = text(val, station_name, sung_name, status_text, line_name, currentFileCount);
		$('div.selected-list').append(element);

		currentFileCount += 1;
		totalManageElement.attr('value', currentFileCount);
	}

	function text(val, station_name, sung_name, status_text, line_name, currentFileCount) {
		t = "<div class='station_form'><div class='station-content'>"
		t += "<div class='station-relation'><input type='hidden' name='stationinmovie-" + currentFileCount + "-id' id='id_stationinmovie-" + currentFileCount + "-id'>"
		t += "<input type='hidden' name='stationinmovie-" + currentFileCount + "-sort_by_part' class='sort_by_part' id='id_stationinmovie-" + currentFileCount + "-sort_by_part'>"

		t += "<input type='hidden' class='get_group_station' value='" + get_group_station + "'>"
		t += "<input type='hidden' class='line_service_pk' value='" + line_service_pk + "'>"
		t += "<input type='hidden' class='line_customize_name' value=''>"
		t += "<input type='hidden' class='category' value='" + category + "'>"
		t += "<input type='hidden' class='pref' value='" + pref + "'>"
		t += "<input type='hidden' class='get_color' value='" + get_color + "'>"
		t += "<input type='hidden' class='is_representative' value='" + is_representative + "'>"
		t += "<input type='hidden' class='other_option' value='" + other_option + "'>"

		t += "<input type='hidden' name='stationinmovie-" + currentFileCount + "-line_service_on_other_options' class='line_service_on_other_options' id='id_stationinmovie-" + currentFileCount + "-line_service_on_other_options'>"
		t += "<input type='hidden' name='stationinmovie-" + currentFileCount + "-line_name_customize' class='line_name_customize' id='id_stationinmovie-" + currentFileCount + "-line_name_customize'>"

		t += "<div class='station-relation-line'></div>"
		t += "<div class='station-relation-select'><select name='stationinmovie-" + currentFileCount + "-back_rel' class='back_rel' id='id_stationinmovie-" + currentFileCount + "-back_rel'>"
		t += "<option value='0'>強制的につなげる</option><option value='1' selected>通常接続</option><option value='2'>強制的に離す</option>"
		t += "</select></div></div>"

		t += "<div class='station-box'>"
		t += "<div class='station-sortable'><a class='sortable-handle'><i class='fas fa-bars'></i></a></div>"
		t += "<div class='station-line-search'><a class='station-line-search-button'>路線検索</a></div>"

		t += "<div class='station-info'><div class='station-info-top'><input type='hidden' name='stationinmovie-" + currentFileCount + "-station_service' class='station_service' id='id_stationinmovie-" + currentFileCount + "-station_service' value='" + val + "'>"
		t += "<div class='station-name-fixed'>" + station_name + "</div>"
		t += "<div class='station-line-name'>" + line_name + "</div>"
		t += "</div>"
		t += "<div class='station-info-bottom'>"
		t += "<div class='station-sung-name'>歌唱名：<input type='text' name='stationinmovie-" + currentFileCount + "-sung_name' class='sung_name' maxlength='400' id='id_stationinmovie-" + currentFileCount + "-sung_name' value='" + sung_name + "'></div>"
		t += "<div class='station-explanation'>備考：<input type='text' name='stationinmovie-" + currentFileCount + "-explanation' class='explanation' id='id_stationinmovie-" + currentFileCount + "-explanation' value='" + status_text + "'></div></div></div>"
		t += "<div class='station-delete'><a class='sortable-delete'><input type='checkbox' name='stationinmovie-" + currentFileCount + "-DELETE' id='id_stationinmovie-" + currentFileCount + "-DELETE' style='display: none;'><i class='fas fa-times'></i></a></div>"
		t += "</div></div></div>"
		return t
	}

	$('div.selected-list').sortable({
		handle: ".sortable-handle",
		update: function() {
			$('.station_form').each(function(i, form) {
				$(form).find('.sort_by_part').val(i);
			})
		}
	})

	$(document).on('click', '.sortable-delete', function() {
		$(this).find('input').prop('checked', true);
		$(this).parents(".station_form").hide();
	})
})

// 路線編集モーダル
stations = []
stations_for_display = []

$('#line-customize-modal-open').click(function() {
	$(this).blur();
	if ($('#line-customize-modal-overlay')[0]) return false;

	$('.station_form').each(function(i, form) {
		$(form).find('.sort_by_part').val(i);
	})

	stations = []
	i = 0;
	$("#selected-list .station_form").each(function(index, val) {
		stations[i] = {}
		stations[i].sort_by_part = $(val).find('.sort_by_part').val()
		stations[i].station_service_pk = $(val).find('.station_service').val()
		stations[i].station_service_name = $(val).find('.station-name-fixed').html()
		stations[i].sung_name = $(val).find('.sung_name').val()
		stations[i].get_group_station = $(val).find('.get_group_station').val()
		stations[i].line_service_pk = $(val).find('.line_service_pk').val()
		stations[i].line_service_name = $(val).find('.station-line-name').html()

		cust = $(val).find('.line_name_customize').val()
		stations[i].line_name_customize = (cust == "") ? $(val).find('.station-line-name').html() : cust

		stations[i].line_service_on_other_options = $(val).find('.line_service_on_other_options').val()
		stations[i].back_rel = $(val).find('.back_rel').val()
		stations[i].category = $(val).find('.category').val()
		stations[i].pref = $(val).find('.pref').val()
		stations[i].get_color = $(val).find('.get_color').val()
		stations[i].is_representative = $(val).find('.is_representative').val()
		stations[i].other_option = $(val).find('.other_option').val()
		stations[i].explanation = $(val).find('.explanation').val()
		stations[i].is_delete = $(val).find('.sortable-delete').find('input').prop('checked')
		i++;
	})
	// $('#station-line-list').val(text)
	
	line_name_customize_editing_index = undefined;
	$('#line-name-customize-detail-editor').empty()
	other_option_editing_index = undefined;
	$('#other_option-line-detail-editor').empty()

	$('.line-name-customize-option-active').removeClass('line-name-customize-option-active');
	$('.other_option-line-option-active').removeClass('other_option-line-option-active');

	generate_line_name_customize_editor();
	generate_other_option_line_editor();
	generate_stations_for_display();
	station_display(0);

	$('body').append("<div id='line-customize-modal-overlay'></div>");
	$('#line-customize-modal-overlay').fadeIn("fast");

	centeringModalSyncer($("#line-customize-modal-content"));
	$('#line-customize-modal-content').fadeIn("fast");

	$("#line-customize-modal-close").unbind().click(function() {
		$("#line-customize-modal-content, #line-customize-modal-overlay").fadeOut("fast", function() {
			$("#line-customize-modal-overlay").remove();
		})
	})

	$("#line-customize-modal-determine").unbind().click(function() {
		$("#line-customize-modal-content, #line-customize-modal-overlay").fadeOut("fast", function() {
			$("#line-customize-modal-overlay").remove();
		})
		line_customize_determine();
	})
})

$(window).resize(centeringModalSyncer($("#line-customize-modal-content")))

function centeringModalSyncer(modalContent) {
	var w = window.innerWidth;
	var h = window.innerHeight;
	var cw = modalContent.outerWidth();
	var ch = modalContent.outerHeight();
	var pxleft = ((w-cw)/2);
	var pxtop = ((h-ch)/2);
	modalContent.css({"left": pxleft + "px"});
	modalContent.css({"top": pxtop + "px"});
}

//路線設定モーダルでタブを切り替えた時の挙動
$(function() {
	$('.modal-tab').click(function() {
		line_name_customize_editing_index = undefined;
		$('#line-name-customize-detail-editor').empty()
		other_option_editing_index = undefined;
		$('#other_option-line-detail-editor').empty()

		$('.line-name-customize-option-active').removeClass('line-name-customize-option-active');
		$('.other_option-line-option-active').removeClass('other_option-line-option-active');

		$('.modal-is-active').removeClass('modal-is-active');
		$(this).addClass('modal-is-active');
		$('.modal-is-show').removeClass('modal-is-show');
		const index = $(this).index();
		$('.modal-tab-content').eq(index).addClass('modal-is-show');
	})
})

function generate_stations_for_display() {
	stations_for_display = []

	prev_line = undefined
	now_line = undefined
	prev_line_name = undefined
	now_line_name = undefined

	$(stations).each(function(i, data) {
		if (data.is_delete) return true;
		if (toBoolean(data.other_option)) {
			if (data.line_service_on_other_options != "") { //その他オプションで、所属路線が変更されていた場合
				now_line = data.line_service_on_other_options;
			} else { //その他オプションで、所属路線が変更されていない場合（廃駅としてのオプションを適用）
				now_line = data.line_service_pk;
			}
		} else {
			now_line = data.line_service_pk
		}
		now_line_name = data.line_service_name;
		if (data.line_name_customize) now_line_name = data.line_name_customize;
		if (prev_line != now_line || prev_line_name != now_line_name || data.back_rel == 2) stations_for_display.push([])
		stations_for_display[stations_for_display.length - 1].push(data)
		prev_line = now_line;
		prev_line_name = now_line_name;
	})
}

stations_for_line_name_customize_editor = []

function generate_line_name_customize_editor() { //路線名カスタマイズ、路線表示
	stations_for_line_name_customize_editor = []
	$('#line-name-customize-selector').empty();

	prev_line = undefined
	now_line = undefined

	$(stations).each(function(i, data) {
		if (data.is_delete) return true;
		if (toBoolean(data.other_option)) {
			if (data.line_service_on_other_options != "") { //その他オプションで、所属路線が変更されていた場合
				now_line = data.line_service_on_other_options;
			} else { //その他オプションで、所属路線が変更されていない場合（廃駅としてのオプションを適用）
				now_line = data.line_service_pk;
			}
		} else {
			now_line = data.line_service_pk
		}
		if (prev_line != now_line || data.back_rel == 2) stations_for_line_name_customize_editor.push([])
		stations_for_line_name_customize_editor[stations_for_line_name_customize_editor.length - 1].push(data)
		prev_line = now_line;
	})


	$(stations_for_line_name_customize_editor).each(function(l, line) {
		$(line).each(function(s, station) {
			line_name = station.line_service_name
			if (toBoolean(station.other_option) == false) {
				return false;
			}
		})
		text = line[0].sung_name + "～" + line[line.length-1].sung_name + "<br><small>" + line_name + "</small>"
		if (line.length-1 == 0) text = line[0].sung_name + "<br><small>" + line_name + "</small>"
		$('#line-name-customize-selector').append("<div class='line-name-customize-option'>" + text + "</div>");
	})
}

//駅ごとのオプション生成
function generate_line_customize_option(sung_name, explanation, line_customize_name) {
	o = "<div class='line-name-customize-detail-station-option'>"
	o += "<div class='line-name-customize-detail-station-name'>" + sung_name + "<small>" + explanation + "</small></div>"
	o += "<div><input type='textbox' class='line-name-customize-input' value='" + line_customize_name + "'></div>"
	o += "</div>"
	return o;
}

//駅オプションのリストHTML生成
function generate_line_customize_station_option_list() {
	$('#line-name-customize-detail-editor').empty()

	editor_inner = "<div id='line-name-customize-detail-controller'>"
	editor_inner += "<input type='textbox' class='line-name-customize-all-input'> <button class='line-name-customize-all-button'>まとめて設定</button>"
	editor_inner += "<br><button class='line-name-customize-reset'>リセット</button>"
	editor_inner += "</div>"
	editor_inner += "<div>駅ごとに設定<small> （高度な設定）</small></div>"
	editor_inner += "<div id='line-name-customize-detail-station-list'></div>"
	$('#line-name-customize-detail-editor').append(editor_inner)

	$(stations_for_line_name_customize_editor[line_name_customize_editing_index]).each(function(s, station) {
		option = generate_line_customize_option(station.sung_name, station.explanation, station.line_name_customize);
		$('#line-name-customize-detail-station-list').append(option)
	})
}

line_name_customize_editing_index = undefined

$(function() {
	//路線名カスタマイズで路線をクリックしたとき
	$(document).on('click', '.line-name-customize-option', function() {
		$('.line-name-customize-option-active').removeClass('line-name-customize-option-active');
		$(this).addClass("line-name-customize-option-active")

		line_name_customize_editing_index = $(this).index();
		generate_line_customize_station_option_list();
	})

	// 駅のカスタマイズ路線名を変更したとき
	$(document).on('change', '.line-name-customize-input', function() {
		station_index = $(this).parents('.line-name-customize-detail-station-option').index();

		changing_station = stations_for_line_name_customize_editor[line_name_customize_editing_index][station_index]

		stations[changing_station.sort_by_part].line_name_customize = $(this).val();

		generate_stations_for_display();
		station_display(0);
	})

	// 駅のカスタマイズ路線名をまとめて変更したとき
	$(document).on('click', '.line-name-customize-all-button', function() {
		val = $('.line-name-customize-all-input').val();

		$(stations_for_line_name_customize_editor[line_name_customize_editing_index]).each(function(s, station) {
			stations[station.sort_by_part].line_name_customize = val;
		})

		generate_line_customize_station_option_list();
		generate_stations_for_display();
		station_display(0);
	})

	//駅のカスタマイズ路線名リセット
	$(document).on('click', '.line-name-customize-reset', function() {
		$(stations_for_line_name_customize_editor[line_name_customize_editing_index]).each(function(s, station) {
			line_name = station.line_service_name
			if (toBoolean(station.other_option) == false) {
				return false;
			}
		})

		$(stations_for_line_name_customize_editor[line_name_customize_editing_index]).each(function(s, station) {
			stations[station.sort_by_part].line_name_customize = line_name;
		})

		generate_line_customize_station_option_list();
		generate_stations_for_display();
		station_display(0);
	})

})

stations_for_other_option_line_editor = []

function generate_other_option_line_editor() { //廃駅などの路線設定
	stations_for_other_option_line_editor = []
	$('#other_option-line-selector').empty()

	prev_line = undefined
	now_line = undefined

	$(stations).each(function(i, data) {
		if (data.is_delete) return true;
		now_line = data.line_service_pk
		if (prev_line != now_line || data.back_rel == 2 || toBoolean(data.is_representative)) stations_for_other_option_line_editor.push([])
		stations_for_other_option_line_editor[stations_for_other_option_line_editor.length - 1].push(data)
		prev_line = now_line;
	})


	$(stations_for_other_option_line_editor).each(function(l, line) {
		text = line[0].sung_name + "～" + line[line.length-1].sung_name + "<br><small>" + line[0].line_service_name + "</small>"
		if (line.length-1 == 0) text = line[0].sung_name + "<br><small>" + line[0].line_service_name + "</small>"
		disable_class = (toBoolean(line[0].other_option) == false || toBoolean(line[0].is_representative)) ? " is-disable" : ""
		$('#other_option-line-selector').append("<div class='other_option-line-option" + disable_class + "'>" + text + "</div>");
	})
}

//駅ごとのオプション生成
function generate_other_option_option(sung_name, explanation, before, after) {
	b =  (before) ? " other_option-detail-station-before-set-active" : ""
	a =  (after) ? " other_option-detail-station-after-set-active" : ""
	o = "<div class='other_option-detail-station-option'>"
	o += "<div class='other_option-detail-station-name'>" + sung_name + "<small>" + explanation + "</small></div>"
	o += "<div class='other_option-detail-station-before-set" + b + "'><div>▼</div></div>"
	o += "<div class='other_option-detail-station-after-set" + a + "'><div>▲</div></div>"
	o += "</div>"
	return o;
}

//駅オプションのリストHTML生成
function generate_other_option_station_option_list() {
	$('#other_option-line-detail-editor').empty()

	prev = stations_for_other_option_line_editor[other_option_editing_index-1]
	prev = (prev) ? prev[stations_for_other_option_line_editor[other_option_editing_index-1].length-1] : {}
	next = stations_for_other_option_line_editor[other_option_editing_index+1]
	next = (next) ? next[0] : {}

	before_name = (prev.line_service_name) ? prev.line_service_name : "(なし)"
	after_name = (next.line_service_name) ? next.line_service_name : "(なし)"
	editor_inner = "<div id='other_option-detail-controller'>"
	editor_inner += "<button id='other_option-reset'>リセット</button>"
	editor_inner += "</div>"
	editor_inner += "<div class='other_option-surround-line-name'>前の路線：<span class='before-name'>" + before_name + "</span></div>"
	editor_inner += "<div id='other_option-detail-station-list'></div>"
	editor_inner += "<div class='other_option-surround-line-name'>次の路線：<span class='after-name'>" + after_name + "</span></div>"
	$('#other_option-line-detail-editor').append(editor_inner)

	generate_other_option_station_option_list_inner();
}

//駅リスト内部の生成
function generate_other_option_station_option_list_inner() {
	$('#other_option-detail-station-list').empty()

	prev = stations_for_other_option_line_editor[other_option_editing_index-1]
	prev = (prev) ? prev[stations_for_other_option_line_editor[other_option_editing_index-1].length-1] : {}
	next = stations_for_other_option_line_editor[other_option_editing_index+1]
	next = (next) ? next[0] : {}

	$(stations_for_other_option_line_editor[other_option_editing_index]).each(function(s, station) {
		before = station.line_service_on_other_options == prev.line_service_pk
		after = station.line_service_on_other_options == next.line_service_pk
		option = generate_other_option_option(station.sung_name, station.explanation, before, after);
		$('#other_option-detail-station-list').append(option)
	})
}

other_option_editing_index = undefined;

$(function() {
	//廃駅などの路線設定で路線をクリックしたとき
	$(document).on('click', '.other_option-line-option', function() {
		if ($(this).hasClass('is-disable')) {
			return false;
		}
		$('.other_option-line-option-active').removeClass('other_option-line-option-active');
		$(this).addClass("other_option-line-option-active")
		other_option_editing_index = $(this).index();
		generate_other_option_station_option_list();
	})

	// //前後の路線と同じにする をクリックしたとき
	// $(document).on('click', '#same-before-after', function() {
	// 	const prev = stations_for_other_option_line_editor[other_option_editing_index-1][stations_for_other_option_line_editor[other_option_editing_index-1].length-1]
	// 	$(stations_for_other_option_line_editor[other_option_editing_index]).each(function(s, station) {
	// 		stations[station.sort_by_part].line_service_on_other_options = prev.line_service_pk;
	// 		stations[station.sort_by_part].line_name_customize = prev.line_service_name;
	// 	})
	// 	generate_station_option_list();
	// 	generate_stations_for_display();
	// 	station_display(0);
	// })

	//前の路線設定のボタン(各駅に存在) をクリックしたとき
	$(document).on('click', '.other_option-detail-station-before-set', function() {
		station_index = $(this).parents('.other_option-detail-station-option').index();

		emp = {line_service_pk: "", line_service_name: ""}
		prev = stations_for_other_option_line_editor[other_option_editing_index-1]
		prev = (prev) ? prev[stations_for_other_option_line_editor[other_option_editing_index-1].length-1] : emp

		$(stations_for_other_option_line_editor[other_option_editing_index]).each(function(s, station) {
			if (s > station_index) {
				if (station.line_service_on_other_options != prev.line_service_pk) return false;
				stations[station.sort_by_part].line_service_on_other_options = "";
				stations[station.sort_by_part].line_name_customize = "";
			} else {
				stations[station.sort_by_part].line_service_on_other_options = prev.line_service_pk;
				stations[station.sort_by_part].line_name_customize = prev.line_service_name;
			}
		})
		generate_line_name_customize_editor();
	generate_other_option_station_option_list_inner();
		generate_stations_for_display();
		station_display(0);		
	})

	//後の路線設定のボタン(各駅に存在) をクリックしたとき
	$(document).on('click', '.other_option-detail-station-after-set', function() {
		station_index = $(this).parents('.other_option-detail-station-option').index();

		emp = {line_service_pk: "", line_service_name: ""}
		next = stations_for_other_option_line_editor[other_option_editing_index+1]
		next = (next) ? next[0] : emp

		tmp_stations = []
		$(stations_for_other_option_line_editor[other_option_editing_index]).each(function(s, station) {
			tmp_stations.push(station);
		})
		tmp_stations.reverse();

		$(tmp_stations).each(function(s, station) {
			if (s > tmp_stations.length - 1 - station_index) {
				if (station.line_service_on_other_options != next.line_service_pk) return false;
				stations[station.sort_by_part].line_service_on_other_options = "";
				stations[station.sort_by_part].line_name_customize = "";
			} else {
				stations[station.sort_by_part].line_service_on_other_options = next.line_service_pk;
				stations[station.sort_by_part].line_name_customize = next.line_service_name;
			}
		})
		generate_line_name_customize_editor();
	generate_other_option_station_option_list_inner();
		generate_stations_for_display();
		station_display(0);
	})

	//リセットボタンをクリックしたとき
	$(document).on('click', '#other_option-reset', function() {
		$(stations_for_other_option_line_editor[other_option_editing_index]).each(function(s, station) {
			stations[station.sort_by_part].line_service_on_other_options = "";
			stations[station.sort_by_part].line_name_customize = "";
		})
		generate_line_name_customize_editor();
	generate_other_option_station_option_list_inner();
		generate_stations_for_display();
		station_display(0);
	})

})

parturl = []
lineurl = []
stationurl = []

function key_station_text(beforecolor, aftercolor, stationid, stationservicename, linename, stationsungname, explanation, end) {
	if (explanation) {
		title = stationsungname + "" + explanation + " 【" + stationservicename + " - " + linename + "】"
	} else {
		title = stationsungname + " 【" + stationservicename + " - " + linename + "】"
	}

	if (end) {
		return "<div class='key-station key-station-end' title='" + title + "'><div class='key-station-icon'></div><div class='station-before' style='background: " + beforecolor + "'></div><div class='station-after' style='background: " + aftercolor + "'></div><a href='" + stationurl[0] + stationid + stationurl[1] + "'>" + stationsungname + "<small>" + explanation + "</small></a></div>";
	} else {
		return "<div class='key-station' title='" + title + "'><div class='key-station-icon'></div><div class='station-before' style='background: " + beforecolor + "'></div><div class='station-after' style='background: " + aftercolor + "'></div><a href='" + stationurl[0] + stationid + stationurl[1] + "'>" + stationsungname + "<small>" + explanation + "</small></a></div>";
	}
}

function line_box_text(lineid, beforecolor, aftercolor, linename, linecustomizename, icon, other_option, button) {
	button_parts = (button) ? "<i class='fas fa-play line-button'></i>" : ""
	if (linename != linecustomizename && linecustomizename) {
		linename = linecustomizename + "<br><small>" + linename + "</small>"
	}
	return "<div><div class='line-box'><a href='" + lineurl[0] + lineid + lineurl[1] + "'><div class='line-before' style='background: " + beforecolor + "'></div><div class='line-after' style='background: " + aftercolor + "'></div><div class='line-icon'><i class='fas fa-" + icon + "'></i></div><div class='line-name'>" + linename + "</div></a><div class='line-button-container'>" + button_parts + "</div></div>";
}

function station_ul_text(id, ul) {
	return "<ul class='station-ul station-ul-" + id + "-" + ul + "'></ul></div>";
}

function station_text_f(beforecolor, aftercolor, stationid, stationservicename, linename, stationsungname, explanation) {
	if (explanation) {
		title = stationsungname + "" + explanation + " 【" + stationservicename + " - " + linename + "】"
	} else {
		title = stationsungname + " 【" + stationservicename + " - " + linename + "】"
	}

	return "<li class='station-name' title='" + title + "'><div class='station-before' style='background: " + beforecolor + "'></div><div class='station-after' style='background: " + aftercolor + "'></div><a href='" + stationurl[0] + stationid + stationurl[1] + "'>" + stationsungname + "<small>" + explanation + "</small></a></li>";
}

function toBoolean(data) {
	if ($.type(data) == "boolean") return data
	return data.toLowerCase() === 'true';
}

function station_parody_display(id, stations) {
	ul = 0;

	parody_station_head = line_box_text(undefined, "#333", "#333", "駅名替え歌", "駅名替え歌", stations[0].category, false, true)
	$('.station-list-' + id).append("<div class='parody-edge'></div>" + parody_station_head + "<ul class='station-ul station-ul-" + id + "-" + ul + "' style='display: block;'></ul></div>")

	$(stations).each(function(i, station) {
		name = (station.explanation == null) ? station.sung_name : station.sung_name + "<small>" + station.explanation + "</small>"
		linename = (station.line_name_customize == null) ? station.line_service_name : station.line_name_customize
		parody_station = "<div class='parody-station'><a href='" + stationurl[0] + station.station_service_pk + stationurl[1] + "' style='border-color: " + station.get_color + "'><div class='parody-station-name'>" + name + "</div><div class='parody-line-name'>" + linename + "</div><div class='parody-pref-name'>" + station.pref + "</div></a></div>";
	 	$('.station-ul-' + id + "-" + ul).append(parody_station)
	})
	
	parody_station_tail = "<div class='parody-edge'></div>"
	$('.station-list-' + id).append(parody_station_tail);
}

function station_display(id) {
	station_list = $('#station-display-check .station-list');
	station_list.empty();

	var ul = 0;
	$(stations_for_display).each(function(l, line) {

		$(line).each(function(s, station) {
			line_name = station.line_service_name
			if (toBoolean(station.other_option) == false) {
				return false;
			}
			line_name = ""
		})

		$(line).each(function(s, station) {
			var prev_color = "none", now_color = station.get_color

			function start_station() {
				key_station = key_station_text(prev_color, now_color, station.station_service_pk, station.station_service_name, line_name, station.sung_name, station.explanation, false)
				line_box = line_box_text(station.line_service_pk, station.get_color, station.get_color, line_name, station.line_name_customize, station.category, station.other_option, true)
				station_ul = station_ul_text(id, ul);
				station_list.append(key_station + line_box + station_ul);
			}

			function end_station() {
				key_station = key_station_text(now_color, "none", station.station_service_pk, station.station_service_name, line_name, station.sung_name, station.explanation, true)
				station_list.append(key_station);
			}
			function middle_station() {
				station = station_text_f(prev_color, station.get_color, station.station_service_pk, station.station_service_name, line_name, station.sung_name, station.explanation)
				$('.station-ul-' + id + '-' + ul).append(station)
			}

			prev = line[s-1];
			next = line[s+1];
			if (s == 0) {
				if (l == 0) {
					prev = {} //駅一覧の1番最初
				} else {
					prev = stations_for_display[l-1][stations_for_display[l-1].length-1] //路線ごとの最初の時、1つ前の路線の最後の駅を取得
				}
			}
			if (s == line.length-1) {
				if (l == stations_for_display.length-1) {
					next = {} //駅一覧の1番最後
				} else {
					next = stations_for_display[l+1][0] //路線ごとの最後の時、1つ後の路線の最初の駅を取得
				}
			}

			if (toBoolean(station.is_representative)) { //路線代表オブジェクトの時
				rep_line = line_box_text(station.line_service_pk, station.get_color, station.get_color, station.explanation, station.sung_name, station.category, station.other_option, false)
				station_list.append("<div class='parody-edge'></div>" + rep_line + "<div class='parody-edge parody-edge-end'></div>")
				return true;
			}

			is_prev_same_group = (toBoolean(station.other_option) == false && prev.get_group_station == station.get_group_station)
			
			if (next.other_option != undefined) {
				is_next_same_group = (toBoolean(next.other_option) == false && next.get_group_station == station.get_group_station)
			} else {
				is_next_same_group = false;
			}
			

			// 開始駅かどうかの判定
			is_key_start = ((s == 0 && !is_prev_same_group && station.back_rel != 0) || station.back_rel == 2)
			// 終了駅かどうかの判定
			is_key_end = ((s == line.length-1 && !is_next_same_group) || next.back_rel == 2)

			if (next.back_rel == 0) { //次の駅が「強制的につなげる」の時
				prev_color = prev.get_color;
				if (is_key_start) prev_color = "none";
				key_station = key_station_text(prev_color, station.get_color, station.station_service_pk, station.station_service_name, line_name, station.sung_name, station.explanation, false)
				line_box_before = line_box_text(station.line_service_pk, station.get_color, station.get_color, line_name, station.line_name_customize, station.category, station.other_option, false)
				line_box_after = line_box_text(next.line_service_pk, next.get_color, next.get_color, next.line_service_name, next.line_name_customize, next.category, next.other_option, false)
				station_ul = station_ul_text(id, ul);
				station_list.append(key_station + line_box_before + line_box_after + station_ul);
				ul++;
				return true;
			}

			if (station.back_rel == 0) { //現在の駅が「強制的につなげる」の時
				prev_color = station.get_color;
				if (is_key_end) {
					end_station();
				} else {
					if (next.back_rel != 0 && next.get_group_station != station.get_group_station) start_station();
				}
				return true;
			}

			if (s == line.length-1) {
				if (is_key_start) now_color = "none";
				if (is_key_end) end_station();
				ul++;
				return true;
			}

			if (s == 0) {
				if (!is_key_start) prev_color = prev.get_color;
				start_station();
				return true;
			}

			prev_color = station.get_color;
			if ((station.station_service_pk != next.station_service_pk) && (station.get_group_station == next.get_group_station)) {
				return true;
			} else if ((station.station_service_pk != prev.station_service_pk) && (station.get_group_station == prev.get_group_station)) {
				prev_color = prev.get_color;
			}
			middle_station();
		})
	})
console.log(stations_for_display)
}


$(function() {
	$(document).on('click', '.line-button-container', function() {
		$(this).parent().next('.station-ul').slideToggle(400, buttonFunc);
	})

	function buttonFunc() {
		if($(this).css('display') == 'none') {
			$(this).prev('.line-box').find('.line-button').removeClass("open-button")
		} else {
			$(this).prev('.line-box').find('.line-button').addClass("open-button")
		}
	}
})

function line_customize_determine() {
	$(stations).each(function(index, station) {
		station_form = $("#selected-list .station_form").eq(index)
		station_form.find('.line_service_on_other_options').val(station.line_service_on_other_options)
		station_form.find('.line_name_customize').val(station.line_name_customize)
	})
}

$('.submit-button').on('click', function() {
	$(this).prop('disabled', true);
	$(this).addClass("submit-button-disabled")
	$(this).html('<div class="loading"></div>');
})