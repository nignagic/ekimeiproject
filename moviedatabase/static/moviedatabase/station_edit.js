//YouTubeジャンプ
$('.youtube-jump').on('click', function() {
	time = $(this).prev('.start_time').val()
	console.log(time)
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
})

//曲・ボーカル追加
function add_name(name, pk) {
	var select = $('select.participant')[0];
	var option = document.createElement('option');
	option.setAttribute('value', pk);
	option.innerHTML = name;

	select.add(option, 0);
	select.options[0].selected = true;
}

function add_song(name, pk) {
	var select = $('select.song')[0];
	var option = document.createElement('option');
	option.setAttribute('value', pk);
	option.innerHTML = name;

	select.add(option, 0);
	select.options[0].selected = true;
}

function add_vocalnew(name, pk) {
	var select = $('select.vocalnew')[0];
	var option = document.createElement('option');
	option.setAttribute('value', pk);
	option.innerHTML = name;

	select.add(option, 0);
	select.options[0].selected = true;
}

// 都道府県を選択したときの挙動
$('#pref-select').children('div').on('click', function() {
	pref = $(this).attr('value');
	var s = "/api/pref/" + pref + "/lineservice/?format=json";
	$(".pref-line-select").empty();
	$.getJSON(s, function(data) {
		for (var i in data) {
			var op_line = "<div value='" + data[i].line_service_pk + "' class='line-option'>" + data[i].__str__ + "</div>";
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
			var op_line = "<div value='" + data[i].line_service_pk + "' class='line-option'>" + data[i].__str__ + "</div>";
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
			var op_station = "<option value='" + data[i].station_service_pk + "' data-name='" + data[i].__str__ + "' data-line='" + data[i].line_service_name + "' class='station-option'>" + data[i].__str__ + "</option>"
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
$(document).on('click', '.line-search-button', function() {
	station = $(this).parents('.stations-box').find('.station_service').attr("value");
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
		$('.is-active').removeClass('is-active');
		$(this).addClass('is-active');
		$('.is-show').removeClass('is-show');
		const index = $(this).index();
		$('.tab-content').eq(index).addClass('is-show');
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
			var op_station = "<option value='" + data[i].station_service_pk + "' data-name='" + data[i].__str__ + "' data-line='" + data[i].line_service_name + "' class='station-option'>" + data[i].__str__ + " ‐ " + data[i].line_service_name + "</option>"
			$('.station-select').append(op_station)
		}
	})
}
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

	var totalManageElement = $('input#id_stationinmovie_set-TOTAL_FORMS');
	var currentFileCount = parseInt(totalManageElement.val());

	$(document).on('click', '.station-append', function() {
		$('.station-select option:selected').each(function() {
			station_append(this);
		})

		$('.station_form').each(function(i, form) {
			$(form).find('.sort_by_part').val(i);
		})
	})

	$(document).on('dblclick', '.station-option', function() {
		station_append(this)

		$('.station_form').each(function(i, form) {
			$(form).find('.sort_by_part').val(i);
		})
	})

	function station_append(station) {
		val = $(station).attr("value");
		name = $(station).data('name');
		line_name = $(station).data('line');

		var element = text(val, name, line_name, currentFileCount);
		$('div.selected-list').append(element);

		currentFileCount += 1;
		totalManageElement.attr('value', currentFileCount);

		$('.selected-list').scrollTop($('.selected-list')[0].scrollHeight);
	}

	function text(val, name, line_name, currentFileCount) {
		e = "<div class='station_form'><div class='stations'><div class='stations-handle'><a class='sortable-handle'>■</a></div><div class='stations-content'>"
		e += "<div class='stations-relation'>"
		e += "<input type='hidden' name='stationinmovie_set-" + currentFileCount + "-id' value='' id='id_stationinmovie_set-" + currentFileCount + "-id'>"
		e += "<input type='hidden' name='stationinmovie_set-" + currentFileCount + "-sort_by_part' value='' class='sort_by_part' id='id_stationinmovie_set-" + currentFileCount + "-sort_by_part'>"
		e += "<div class='stations-relation-line'></div>"
		e += "<div class='stations-relation-select'>"
		e += "<select name='stationinmovie_set-" + currentFileCount + "-back_rel' id='id_stationinmovie_set-" + currentFileCount + "-back_rel'>"
		e += "<option value='0'>強制的につなげる</option><option value='1' selected>通常接続</option><option value='2'>強制的に離す</option>"
		e += "</select></div></div>"
		e += "<div class='stations-box'>"
		e += "<div class='line-search'><a class='line-search-button'>路線<br>検索</a></div>"
		e += "<div class='stations-info'><div class='stations-info-top'>"
		e += "<input type='hidden' name='stationinmovie_set-" + currentFileCount + "-station_service' value='" + val + "' class='station_service' id='id_stationinmovie_set-" + currentFileCount + "-station_service'>"
		e += "<div class='station-name-container'><div class='station-name-fixed'>" + name + "</div>"
		e += "<div class='stations-remarks'>備考<input type='textbox' name='remarks[]' class='stations-remarks-text'></div></div></div>"
		e += "<div class='stations-info-bottom'><div class='station-sung-name'>"
		e += "歌唱名：<input type='text' name='stationinmovie_set-" + currentFileCount + "-sung_name' value='" + name + "' maxlength='50' id='id_stationinmovie_set-" + currentFileCount + "-sung_name'>"
		e += "</div><div class='line-name'>" + line_name + "</div></div></div>"
		e += "<div class='stations-delete'><a class='sortable-delete'><input type='checkbox' name='stationinmovie_set-" + currentFileCount + "-DELETE' id='id_stationinmovie_set-" + currentFileCount + "-DELETE'>削除</a></div>"
		e += "</div></div></div></div>"
		return e
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