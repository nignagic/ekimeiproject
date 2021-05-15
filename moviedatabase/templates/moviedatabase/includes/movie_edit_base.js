

	$(function() {

		ss = $('#selected_song_in_movie_list .selected_song_in_movie');
		selected_song_in_movie_list = ""
		ss.each(function (i, val) {
			if (i != 0) selected_song_in_movie_list += ","
			selected_song_in_movie_list += val.value
		})
		add_selected_song(selected_song_in_movie_list)

		ps = $('#selected_parent_movie_list .selected_parent_movie');
		selected_parent_movie_list = ""
		ps.each(function (i, val) {
			if (i != 0) selected_parent_movie_list += ","
			selected_parent_movie_list += val.value
		})
		add_selected_movie(selected_parent_movie_list, "parent")

		rs = $('#selected_related_movie_list .selected_related_movie');
		selected_related_movie_list = ""
		rs.each(function (i, val) {
			if (i != 0) selected_related_movie_list += ","
			selected_related_movie_list += val.value
		})
		add_selected_movie(selected_related_movie_list, "related") 
	})

	function add_selected_song(list) {
		songs = list.split(',')
		$('#selected_song_in_movie_list').empty()
		$('#selected_song_in_movie_name').empty();
		if (songs == "") {
			$('#selected_song_in_movie_name').append("未設定");
		} else {
			$.each(songs, function(i, val) {
				txt = "<input type='hidden' name='song' value='" + val + "' class='selected_song_in_movie' id='id_song_" + i + "'>"
				$('#selected_song_in_movie_list').append(txt)

				var s = "/songdata/api/song/" + val + "?format=json";
				n = ""
				$.getJSON(s, function(data) {
					for (var i in data) {
						$("#selected_song_in_movie_name").append(data[i].song_name);
					}
				})
			})
		}
	}

	function add_selected_movie(list, movie_type) {
		movies = list.split(',')
		$('#selected_'+movie_type+'_movie_list').empty()
		$('#selected_'+movie_type+'_movie_name').empty();
		if (movies == "") {
			$('#selected_'+movie_type+'_movie_name').append("未設定");
		} else {
			$.each(movies, function(i, val) {
				txt = "<input type='hidden' name="+movie_type+" value='" + val + "' class='selected_"+movie_type+"_movie' id='id_"+movie_type+"_" + i + "'>"
				$('#selected_'+movie_type+'_movie_list').append(txt)

				var m = "/api/movie/" + val + "?format=json";
				n = ""
				$.getJSON(m, function(data) {
					for (var i in data) {
						$("#selected_"+movie_type+"_movie_name").append(data[i].movie_name);
					}
				})
			})
		}
	}