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

function key_station_text(stationurl, beforecolor, aftercolor, stationid, stationname) {
	return "<div class='key-station'><div class='key-station-icon'></div><div class='station-before' style='background: " + beforecolor + "'></div><div class='station-after' style='background: " + aftercolor + "'></div><a href='" + stationurl + stationid + "'>" + staitonname + "</a></div>";
}

function line_box_text(lineurl, lineid, beforecolor, aftercolor, linename) {
	return "<div><div class='line-box'><a href='" + lineurl + line + "'><div class='line-before' style='background: " + beforecolor + "'></div><div class='line-after' style='background: " + aftercolor + "'></div><div class='line-icon'><img src='/static/ekimeimysql1/channel.jpg'></div><div class='line-name'>" + linename + "</div></a></div>";
}

function station_ul_text(id, ul) {
	return "<ul class='station-ul station-ul-" + id + "-" + ul + "'></ul></div>";
}

function station_text(stationurl, beforecolor, aftercolor, stationid, stationname) {
	return "<li class='station-name'><div class='station-before' style='background: " + beforecolor + "'></div><div class='station-after' style='background: " + aftercolor + "'></div><a href='" + stationurl + stationid + "'>" + stationname + "</a></li>";
}

$(function() {
	$('.part-table').each(function(index, elem) {
		forloop = 0;
		id = $(elem).data('part_id');
		category = $(elem).data('category');
		var s = "http://localhost:8000/moviedatabase/api/partstation/" + id + "/?format=json";
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
						parody_station = "<div class='parody-station'><a href='http://localhost:8000/ekimeimysql1/stationservice/" + data[i].station_service_pk + "' style='border-color: " + data[i].get_color + "'><div class='parody-station-name'>" + station_text + "</div><div class='parody-line-name'>" + data[i].line_service_name + "</div><div class='parody-pref-name'>" + data[i].pref + "</div></a></div>";
					 	$('.station-ul-' + id + "-" + ul).append(parody_station)
						
						if (afterline == undefined) {
							parody_station_tail = "<div class='parody-edge'></div>"
							$('.station-list-' + id).append(parody_station_tail);
						}
					} else if (line != afterline && afterback == "0") {
					// console.log(afterback);
						if (beforeline != 0) {
							color = data[i].get_color;
						} else {
							color = "none";
						}
						ul++;
						// $('.station-list-' + id).append("<h4 class='movie-line-name'>" + data[i].line_service_name + "</h4><ul class='station-ul station-ul-" + forloop + "'></ul>")
						key_station = "<div class='key-station'><div class='key-station-icon'></div><div class='station-before' style='background: " + color + "'></div><div class='station-after' style='background: " + data[i].get_color + "'></div><a href='http://localhost:8000/ekimeimysql1/stationservice/" + data[i].station_service_pk + "'>" + station_text + "</a></div>"
						line_box_before = "<div><div class='line-box'><a href='http://localhost:8000/ekimeimysql1/lineservice/" + line + "'><div class='line-before' style='background: " + data[i].get_color + "'></div><div class='line-after' style='background: " + data[i].get_color + "'></div><div class='line-icon'><img src='/static/ekimeimysql1/channel.jpg'></div><div class='line-name'>" + data[i].line_service_name + "</div></a></div>"
						line_box_after = "<div><div class='line-box'><a href='http://localhost:8000/ekimeimysql1/lineservice/" + data[j].line_service_pk + "'><div class='line-before' style='background: " + data[j].get_color + "'></div><div class='line-after' style='background: " + data[j].get_color + "'></div><div class='line-icon'><img src='/static/ekimeimysql1/channel.jpg'></div><div class='line-name'>" + data[j].line_service_name + "</div></a></div>"						
						$('.station-list-' + id).append(key_station + line_box_before + line_box_after + "<ul class='station-ul station-ul-" + id + "-" + ul + "'></ul></div>");
					} else if (line != beforeline && data[i].station_group_code == beforestationgroup) {
						ul++;
						$('.station-list-' + id + ' .key-station:last').remove();
						// $('.station-list-' + id).append("<h4 class='movie-line-name'>" + data[i].line_service_name + "</h4><ul class='station-ul station-ul-" + forloop + "'></ul>")
						key_station = "<div class='key-station'><div class='key-station-icon'></div><div class='station-before' style='background: " + beforecolor + "'></div><div class='station-after' style='background: " + data[i].get_color + "'></div><a href='http://localhost:8000/ekimeimysql1/stationservice/" + data[i].station_service_pk + "'>" + station_text + "</a></div>"
						line_box = "<div><div class='line-box'><div class='line-button'></div><a href='http://localhost:8000/ekimeimysql1/lineservice/" + line + "'><div class='line-before' style='background: " + data[i].get_color + "'></div><div class='line-after' style='background: " + data[i].get_color + "'></div><div class='line-icon'><img src='/static/ekimeimysql1/channel.jpg'></div><div class='line-name'>" + data[i].line_service_name + "</div></a></div>"
						$('.station-list-' + id).append(key_station + line_box + "<ul class='station-ul station-ul-" + id + "-" + ul + "'></ul></div>");
					} else if (line != beforeline || data[i].back_rel == "2") {
						if (data[i].back_rel == 0) {
							color = data[i].get_color;
						} else {
							color = "none";
						}
						// $('.station-list-' + id).append("<h4 class='movie-line-name'>" + data[i].line_service_name + "</h4><ul class='station-ul station-ul-" + forloop + "'></ul>")
						if (line == afterline) {
							ul++;
							key_station = "<div class='key-station'><div class='key-station-icon'></div><div class='station-before' style='background: " + color + ";'></div><div class='station-after' style='background: " + data[i].get_color + "'></div><a href='http://localhost:8000/ekimeimysql1/stationservice/" + data[i].station_service_pk + "'>" + station_text + "</a></div>"
							line_box = "<div><div class='line-box'><div class='line-button'></div><a href='http://localhost:8000/ekimeimysql1/lineservice/" + line + "'><div class='line-before' style='background: " + data[i].get_color + "'></div><div class='line-after' style='background: " + data[i].get_color + "'></div><div class='line-icon'><img src='/static/ekimeimysql1/channel.jpg'></div><div class='line-name'>" + data[i].line_service_name + "</div></a></div>"
							station_ul = "<ul class='station-ul station-ul-" + id + "-" + ul + "'></ul></div>";
						} else {
							key_station = "<div class='key-station key-station-end'><div class='key-station-icon'></div><div class='station-before' style='background: " + color + ";'></div><div class='station-after' style='background: none;'></div><a href='http://localhost:8000/ekimeimysql1/stationservice/" + data[i].station_service_pk + "'>" + station_text + "</a></div>"
							line_box = "";
							station_ul = "";
						}
						$('.station-list-' + id).append(key_station + line_box + station_ul);
					} else if (afterline != line || afterline == undefined || data[j].back_rel == "2") {
						// console.log(i)
						key_station = "<div class='key-station key-station-end'><div class='key-station-icon'></div><div class='station-before' style='background: " + data[i].get_color + "'></div><div class='station-after' style='background: none'></div><a href='http://localhost:8000/ekimeimysql1/stationservice/" + data[i].station_service_pk + "'>" + station_text + "</a></div>"
						$('.station-list-' + id).append(key_station);
					} else if ((data[i].station_service_pk != data[j].station_service_pk) && (data[i].station_group_code == data[j].station_group_code)) {
						var station = "<li class='station-name'><div class='station-before' style='background: " + data[i].get_color + "'></div><div class='station-after' style='background: " + data[j].get_color + "'></div><a href='http://localhost:8000/ekimeimysql1/stationservice/" + data[i].station_service_pk + "'>" + station_text + "</a></li>";
					 	$('.station-ul-' + id + "-" + ul).append(station)
					} else if ((data[i].station_service_pk != data[j-2].station_service_pk) && (data[i].station_group_code == data[j-2].station_group_code)) {
					 } else {
						var station = "<li class='station-name'><div class='station-before' style='background: " + data[i].get_color + "'></div><div class='station-after' style='background: " + data[i].get_color + "'></div><a href='http://localhost:8000/ekimeimysql1/stationservice/" + data[i].station_service_pk + "'>" + station_text + "</a></li>";
					 	$('.station-ul-' + id + "-" + ul).append(station)
					}
					beforeline = line;
					beforestationgroup = data[i].station_group_code;
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