$(function() {
	$('.part-header').on('click', function() {
		$(this).next('.part-detail-container').slideToggle();
	})
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

	$(document).on('click', '.all-open', function() {
		$('.part-detail-container').slideDown();
		$('.station-ul').slideDown(400, buttonFunc);
	})
	$(document).on('click', '.all-close', function() {
		if ($('.part-detail-container').length != 1)
			$('.part-detail-container').slideUp();
		$('.station-ul').slideUp(400, buttonFunc);
	})

	if ($('.part-detail-container').length == 1)
		$('.part-detail-container').show();
})

$(function() {
	$(document).on('click', '.start-time', function() {
		time = $(this).text();
		player.playVideo();
		player.seekTo(TimetoSecond(time), true);
	})
})

$(function() {
	d = $('.movie-description').text().replace(/<br>/g, '<br>');
	$('.movie-description').html(d)

	var ua = navigator.userAgent;
	if ((ua.indexOf('iPhone') > 0 || ua.indexOf('Android') > 0) && ua.indexOf('Mobile') > 0) {
		$('.youtube-pc').remove()
	} else if (ua.indexOf('iPad') > 0 || ua.indexOf('Android') > 0) {
		$('.youtube-pc').remove()
	} else {
		$('.youtube-mobile').remove()
	}
})

function TimetoSecond(time) {
	t = time.split(':');
	hour = parseInt(t[0]) * 3600;
	minute = parseInt(t[1]) * 60;
	second = parseInt(t[2]);
	return hour + minute + second;
}



parturl = $('#detail-url').data('part').split('0')
lineurl = $('#detail-url').data('line').split('0')
stationurl = $('#detail-url').data('station').split('0')

function key_station_text(beforecolor, aftercolor, stationid, stationservicename, linename, stationsungname, explanation, end) {
	if (explanation) {
		name = stationsungname + "<small>" + explanation + "</small>"
		title = stationsungname + "" + explanation + " 【" + stationservicename + " - " + linename + "】"
	} else {
		name = stationsungname
		title = stationsungname + " 【" + stationservicename + " - " + linename + "】"
	}

	if (end) {
		return "<div class='key-station key-station-end' title='" + title + "'><div class='key-station-icon'></div><div class='station-before' style='background: " + beforecolor + "'></div><div class='station-after' style='background: " + aftercolor + "'></div><a href='" + stationurl[0] + stationid + stationurl[1] + "'>" + name + "</a></div>";
	} else {
		return "<div class='key-station' title='" + title + "'><div class='key-station-icon'></div><div class='station-before' style='background: " + beforecolor + "'></div><div class='station-after' style='background: " + aftercolor + "'></div><a href='" + stationurl[0] + stationid + stationurl[1] + "'>" + name + "</a></div>";
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
		name = stationsungname + "<small>" + explanation + "</small>"
		title = stationsungname + "" + explanation + " 【" + stationservicename + " - " + linename + "】"
	} else {
		name = stationsungname
		title = stationsungname + " 【" + stationservicename + " - " + linename + "】"
	}

	return "<li class='station-name' title='" + title + "'><div class='station-before' style='background: " + beforecolor + "'></div><div class='station-after' style='background: " + aftercolor + "'></div><a href='" + stationurl[0] + stationid + stationurl[1] + "'>" + name + "</a></li>";
}

$(function() {
	$('.part-table').each(function(index, elem) {
		id = $(elem).data('part_id');
		category = $(elem).data('category');
		var part_stations = parturl[0] + id + "/?format=json";
		(function(id, category) {
			$.getJSON(part_stations, function(data) {
				if (category == "駅名替え歌" || category == "その他") {
					station_parody_display(id, data)
				} else {
					station_display(id, generate_stations_for_display(data));
				}
			})
		})(id, category);
	})
})

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

function toBoolean(data) {
	if ($.type(data) == "boolean") return data
	return data.toLowerCase() === 'true';
}

function generate_stations_for_display(stations) {
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

	return stations_for_display;
}

function station_display(id, stations_for_display) {
	station_list = $('.station-list-' + id);

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
				$(station_list).append(key_station + line_box + station_ul);
			}

			function end_station() {
				key_station = key_station_text(now_color, "none", station.station_service_pk, station.station_service_name, line_name, station.sung_name, station.explanation, true)
				$(station_list).append(key_station);
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
	$(station_list).children('.station-loading').remove()
}