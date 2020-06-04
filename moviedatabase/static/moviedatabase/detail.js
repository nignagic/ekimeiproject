$(function() {
	$('.part-header').on('click', function() {
		$(this).next('.part-detail-container').slideToggle();
	})
	$(document).on('click', '.line-button', function() {
		$(this).parent().next('.station-ul').slideToggle();
	})
	$(document).on('click', '.all-open', function() {
		$('.part-detail-container').slideDown();
		$('.station-ul').slideDown();
	})
	$(document).on('click', '.all-close', function() {
		$('.part-detail-container').slideUp();
		$('.station-ul').slideUp();
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
})

function TimetoSecond(time) {
	t = time.split(':');
	hour = parseInt(t[0]) * 3600;
	minute = parseInt(t[1]) * 60;
	second = parseInt(t[2]);
	return hour + minute + second;
}

$(function() {
	img = "<i class='fas fa-bus'></i>";
	img = "<i class='fas fa-store-alt'></i>";
	img = "<i class='fas fa-road'></i>";
	img = "<i class='fas fa-subway'></i>";
	function key_station_text(beforecolor, aftercolor, stationid, stationname, end) {
		if (end) {
			return "<div class='key-station key-station-end'><div class='key-station-icon'></div><div class='station-before' style='background: " + beforecolor + "'></div><div class='station-after' style='background: " + aftercolor + "'></div><a href='" + stationurl[0] + stationid + stationurl[1] + "'>" + stationname + "</a></div>";
		} else {
			return "<div class='key-station'><div class='key-station-icon'></div><div class='station-before' style='background: " + beforecolor + "'></div><div class='station-after' style='background: " + aftercolor + "'></div><a href='" + stationurl[0] + stationid + stationurl[1] + "'>" + stationname + "</a></div>";
		}
	}

	function line_box_text(lineid, beforecolor, aftercolor, linename, icon) {
		if (icon) {
			return "<div><div class='line-box'><div class='line-button'></div><a href='" + lineurl[0] + line + lineurl[1] + "'><div class='line-before' style='background: " + beforecolor + "'></div><div class='line-after' style='background: " + aftercolor + "'></div><div class='line-icon'>" + img + "</div><div class='line-name'>" + linename + "</div></a></div>";
		} else {
			return "<div><div class='line-box'><a href='" + lineurl[0] + line + lineurl[1] + "'><div class='line-before' style='background: " + beforecolor + "'></div><div class='line-after' style='background: " + aftercolor + "'></div><div class='line-icon'>" + img + "</div><div class='line-name'>" + linename + "</div></a></div>";
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
					line = data[i].line_service_pk;
					station_text = data[i].sung_name;
					if (data[j] != undefined) {
						afterline = data[j].line_service_pk;
						afterback = data[j].back_rel;
					} else {
						afterline = undefined;
						afterback = undefined;
					}

					if (category == "駅名替え歌") {
						if (beforeline == 0) {
							ul++;
							parody_station_head = "<div class='parody-edge'></div><div><div class='line-box'><div class='line-button'></div><a><div class='line-before' style='background: #333;'></div><div class='line-after' style='background: #333;'></div><div class='line-icon'><img src='/static/ekimeimysql1/channel.jpg'></div><div class='line-name'>駅名替え歌</div></a></div>"
							$('.station-list-' + id).append(parody_station_head + "<ul class='station-ul station-ul-" + id + "-" + ul + "'></ul></div>")
						}
						parody_station = "<div class='parody-station'><a href='" + stationurl[0] + data[i].station_service_pk + stationurl[1] + "' style='border-color: " + data[i].get_color + "'><div class='parody-station-name'>" + station_text + "</div><div class='parody-line-name'>" + data[i].line_service_name + "</div><div class='parody-pref-name'>" + data[i].pref + "</div></a></div>";
					 	$('.station-ul-' + id + "-" + ul).append(parody_station)
						
						if (afterline == undefined) {
							parody_station_tail = "<div class='parody-edge'></div>"
							$('.station-list-' + id).append(parody_station_tail);
						}
					} else if (data[i].is_representative) {
						rep_line = line_box_text(data[i].line_service_pk, data[i].get_color, data[i].get_color, data[i].line_service_name, category)
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
						line_box_before = line_box_text(line, data[i].get_color, data[i].get_color, data[i].line_service_name, false)
						line_box_after = line_box_text(data[j].line_service_pk, data[j].get_color, data[j].get_color, data[j].line_service_name, false)
						station_ul = station_ul_text(id, ul);
						$('.station-list-' + id).append(key_station + line_box_before + line_box_after + station_ul);
					} else if (line != beforeline && data[i].get_group_station == beforestationgroup) {
						ul++;
						$('.station-list-' + id + ' .key-station:last').remove();
						// $('.station-list-' + id).append("<h4 class='movie-line-name'>" + data[i].line_service_name + "</h4><ul class='station-ul station-ul-" + forloop + "'></ul>")
						key_station = key_station_text(beforecolor, data[i].get_color, data[i].station_service_pk, station_text, false)
						line_box = line_box_text(line, data[i].get_color, data[i].get_color, data[i].line_service_name, true)
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
							line_box = line_box_text(line, data[i].get_color, data[i].get_color, data[i].line_service_name, true)
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