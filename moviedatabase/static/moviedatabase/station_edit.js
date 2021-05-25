//YouTubeジャンプ
$('.youtube-jump').on('click', function() {
	time = $(this).siblings('.start_time').val()
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

	$('.sortable-delete input').prop('checked', false)
	$('.sortable-delete input').hide()

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
		t = "<div class='station_form'><div class='station-content'>"
		t += "<div class='station-relation'><input type='hidden' name='stationinmovie_set-" + currentFileCount + "-id' id='id_stationinmovie_set-" + currentFileCount + "-id'>"
		t += "<input type='hidden' name='stationinmovie_set-" + currentFileCount + "-sort_by_part' class='sort_by_part' id='id_stationinmovie_set-" + currentFileCount + "-sort_by_part'>"
		t += "<div class='station-relation-line'></div>"
		t += "<div class='station-relation-select'><select name='stationinmovie_set-" + currentFileCount + "-back_rel' id='id_stationinmovie_set-" + currentFileCount + "-back_rel'>"
		t += "<option value='0'>強制的につなげる</option><option value='1' selected>通常接続</option><option value='2'>強制的に離す</option>"
		t += "</select></div></div>"

		t += "<div class='station-box'>"
		t += "<div class='station-sortable'><a class='sortable-handle'><i class='fas fa-bars'></i></a></div>"
		t += "<div class='station-line-search'><a class='station-line-search-button'>路線検索</a></div>"

		t += "<div class='station-info'><div class='station-info-top'><input type='hidden' name='stationinmovie_set-" + currentFileCount + "-station_service' class='station_service' id='id_stationinmovie_set-" + currentFileCount + "-station_service' value='" + val + "'>"
		t += "<div class='station-name-fixed'>" + name + "</div>"
		t += "<div class='station-line-name'>" + line_name + "</div>"
		t += "</div>"
		t += "<div class='station-info-bottom'>"
		t += "<div class='station-sung-name'>歌唱名：<input type='text' name='stationinmovie_set-" + currentFileCount + "-sung_name' class='sung_name' maxlength='400' id='id_stationinmovie_set-" + currentFileCount + "-sung_name' value='" + name + "'></div>"
		t += "<div class='station-explanation'>備考：<input type='text' name='stationinmovie_set-" + currentFileCount + "-explanation' class='explanation' id='id_stationinmovie_set-" + currentFileCount + "-explanation'></div></div></div>"
		t += "<div class='station-delete'><a class='sortable-delete'><input type='checkbox' name='stationinmovie_set-" + currentFileCount + "-DELETE' id='id_stationinmovie_set-" + currentFileCount + "-DELETE' style='display: none;'><i class='fas fa-times'></i></a></div>"
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