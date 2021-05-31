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

	$(document).on('click', '.movie-description-button', function() {
		$('.movie-description').removeClass('movie-description-close')
	})
})

$(function() {
	$(document).on('click', '.start-time', function() {
		time = $(this).text();
		console.log(TimetoSecond(time));
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

$(function() {
	function key_station_text(beforecolor, aftercolor, stationid, stationname, end) {
		if (end) {
			return "<div class='key-station key-station-end'><div class='key-station-icon'></div><div class='station-before' style='background: " + beforecolor + "'></div><div class='station-after' style='background: " + aftercolor + "'></div><a href='" + stationurl[0] + stationid + stationurl[1] + "'>" + stationname + "</a></div>";
		} else {
			return "<div class='key-station'><div class='key-station-icon'></div><div class='station-before' style='background: " + beforecolor + "'></div><div class='station-after' style='background: " + aftercolor + "'></div><a href='" + stationurl[0] + stationid + stationurl[1] + "'>" + stationname + "</a></div>";
		}
	}

	function line_box_text(lineid, beforecolor, aftercolor, linename, icon, button) {
		if (button) {
			return "<div><div class='line-box'><a href='" + lineurl[0] + lineid + lineurl[1] + "'><div class='line-before' style='background: " + beforecolor + "'></div><div class='line-after' style='background: " + aftercolor + "'></div><div class='line-icon'><i class='fas fa-" + icon + "'></i></div><div class='line-name'>" + linename + "</div></a><div class='line-button-container'><i class='fas fa-play line-button'></i></div></div>";
		} else {
			return "<div><div class='line-box'><a href='" + lineurl[0] + lineid + lineurl[1] + "'><div class='line-before' style='background: " + beforecolor + "'></div><div class='line-after' style='background: " + aftercolor + "'></div><div class='line-icon'><i class='fas fa-" + icon + "'></i></div><div class='line-name'>" + linename + "</div></a><div class='line-button-container'></div></div>";
		}
	}

	function station_ul_text(id, ul) {
		return "<ul class='station-ul station-ul-" + id + "-" + ul + "'></ul></div>";
	}

	function station_text_f(beforecolor, aftercolor, stationid, stationname) {
		return "<li class='station-name'><div class='station-before' style='background: " + beforecolor + "'></div><div class='station-after' style='background: " + aftercolor + "'></div><a href='" + stationurl[0] + stationid + stationurl[1] + "'>" + stationname + "</a></li>";
	}

	parturl = $('#detail-url').data('part').split('0')
	lineurl = $('#detail-url').data('line').split('0')
	stationurl = $('#detail-url').data('station').split('0')
	console.log(parturl, lineurl, stationurl)
	$('.part-table').each(function(index, elem) {
		forloop = 0;
		id = $(elem).data('part_id');
		category = $(elem).data('category');
		var s = parturl[0] + id + "/?format=json";
		(function(id, category) {
			ul = 0;
			$.getJSON(s, function(data) {
				beforeline = 0;
				beforestationgroup = 0;
				beforecolor = "";
				j = 1;
				color_view = true;
				for (var i in data) {
					line = data[i].other_option ? beforeline : data[i].line_service_pk;
					station_text = data[i].sung_name;
					if (data[j] != undefined) {
						if (data[j+1] != undefined) {
							afterline = data[j].other_option ? data[j+1].line_service_pk : data[j].line_service_pk;
						} else {
							afterline = data[j].other_option ? undefined : data[j].line_service_pk;
						}
						afterback = data[j].back_rel;
					} else {
						afterline = undefined;
						afterback = undefined;
					}

					if (category == "駅名替え歌") {
						if (beforeline == 0) {
							ul++;
							parody_station_head = line_box_text(undefined, "#333", "#333", "駅名替え歌", data[i].category, true)
							$('.station-list-' + id).append("<div class='parody-edge'></div>" + parody_station_head + "<ul class='station-ul station-ul-" + id + "-" + ul + "' style='display: block;'></ul></div>")
						}
						parody_station = "<div class='parody-station'><a href='" + stationurl[0] + data[i].station_service_pk + stationurl[1] + "' style='border-color: " + data[i].get_color + "'><div class='parody-station-name'>" + station_text + "</div><div class='parody-line-name'>" + data[i].line_service_name + "</div><div class='parody-pref-name'>" + data[i].pref + "</div></a></div>";
					 	$('.station-ul-' + id + "-" + ul).append(parody_station)
						
						if (afterline == undefined) {
							parody_station_tail = "<div class='parody-edge'></div>"
							$('.station-list-' + id).append(parody_station_tail);
						}
					} else if (data[i].is_representative) {
						rep_line = line_box_text(data[i].line_service_pk, data[i].get_color, data[i].get_color, station_text, data[i].category, false)
						$('.station-list-' + id).append("<div class='parody-edge'></div>" + rep_line + "<div class='parody-edge parody-edge-end'></div>")
					} else if (line != afterline && afterback == "0") {
					// console.log(afterback);
						if (beforeline != 0) {
							color = data[i].get_color;
						} else {
							color = "none";
						}
						ul++;
						// $('.station-list-' + id).append("<h4 class='movie-line-name'>" + data[i].line_service_name + "</h4><ul class='station-ul station-ul-" + forloop + "'></ul>")
						key_station = key_station_text(color, data[i].get_color, data[i].station_service_pk, station_text, false)
						line_box_before = line_box_text(line, data[i].get_color, data[i].get_color, data[i].line_service_name, data[i].category, false)
						line_box_after = line_box_text(data[j].line_service_pk, data[j].get_color, data[j].get_color, data[j].line_service_name, data[i].category, false)
						station_ul = station_ul_text(id, ul);
						$('.station-list-' + id).append(key_station + line_box_before + line_box_after + station_ul);
					} else if (line != beforeline && data[i].get_group_station == beforestationgroup && !(data[i].back_rel == "2")) {
						ul++;
						$('.station-list-' + id + ' .key-station:last').remove();
						// $('.station-list-' + id).append("<h4 class='movie-line-name'>" + data[i].line_service_name + "</h4><ul class='station-ul station-ul-" + forloop + "'></ul>")
						key_station = key_station_text(beforecolor, data[i].get_color, data[i].station_service_pk, station_text, false)
						line_box = line_box_text(line, data[i].get_color, data[i].get_color, data[i].line_service_name, data[i].category, true)
						station_ul = station_ul_text(id, ul);
						$('.station-list-' + id).append(key_station + line_box + station_ul);
					} else if (line != beforeline || data[i].back_rel == "2") {
						if (data[i].back_rel == 0) {
							color = data[i].get_color;
						} else {
							color = "none";
						}
						if (line == afterline) {
							ul++;
							key_station = key_station_text(color, data[i].get_color, data[i].station_service_pk, station_text, false)
							line_box = line_box_text(line, data[i].get_color, data[i].get_color, data[i].line_service_name, data[i].category, true)
							station_ul = station_ul_text(id, ul);
						} else {
							key_station = key_station_text(color, "none", data[i].station_service_pk, station_text, false)
							line_box = "";
							station_ul = "";
						}
						$('.station-list-' + id).append(key_station + line_box + station_ul);
					} else if (afterline != line || afterline == undefined || data[j].back_rel == "2") {
						key_station = key_station_text(data[i].get_color, "none", data[i].station_service_pk, station_text, true)
						$('.station-list-' + id).append(key_station);
					} else if ((data[i].station_service_pk != data[j].station_service_pk) && (data[i].get_group_station == data[j].get_group_station)) {
					 	station = station_text_f(data[i].get_color, data[j].get_color, data[i].station_service_pk, station_text)
					 	$('.station-ul-' + id + "-" + ul).append(station)
					} else if ((data[i].station_service_pk != data[j-2].station_service_pk) && (data[i].get_group_station == data[j-2].get_group_station)) {
					} else {
						station = station_text_f(data[i].get_color, data[i].get_color, data[i].station_service_pk, station_text)
						$('.station-ul-' + id + "-" + ul).append(station)
					}
					beforeline = line;
					beforestationgroup = data[i].get_group_station;
					beforecolor = data[i].get_color;
					j++;
					color_view = true;
					// console.log(beforeline + " " + line)
				}
				$('.station-list-' + id).append("</ul>")
			})
		})(id, category);
	})
})