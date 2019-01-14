$(function() {
	// WARNING: Trailing slash issues?
	var datasource = $SCRIPT_ROOT + "{f}.json";

	var reports = {
		"report_names": [
			"downloads-en",//"downloads-fr",
			"pages-en",//"pages-fr",
			"videos-en",//"videos-fr"
		],
		"report_to_icon": {
			"downloads-en":"cloud-download","downloads-fr":"cloud-download",
			"pages-en":"file-text","pages-fr":"file-text",
			"videos-en":"file-video","videos-fr":"file-video"			
		}
	};

	var tiles = '';
	var tile = ''
	+'<div data-role="tile" class="bg-{c}" data-size="{s}">'
		+'<span class="badge-top">{v}</span>'
	    +'<span class="mif-{i} icon"></span>'
	    +'<span class="branding-bar">{n}</span>'
	+'</div>'
	+'';   

	var htile = ''
	+'<a href="{h}" data-size="{s}" data-role="tile" class="bg-{c} ani-hover-bounce">'
		+'<span class="badge-top">{v}</span>'
	    +'<span class="mif-{i} icon"></span>'
	    +'<span class="branding-bar">{n}</span>'
	+'</div>'
	+'';   
	
	$tv = $("#tileview");
	$tv.html('');


	var rpticon = "news";
	for (var i = 0; i < reports.report_names.length; i++) {
		rpticon = reports.report_to_icon[reports.report_names[i]]

		$.getJSON( datasource.replace('{f}', reports.report_names[i])).done(
			$.proxy(function(resp) {


				var itemtile = tile;
				itemtile = itemtile.replace('{n}',resp.meta.name);
				itemtile = itemtile.replace('{i}','news');
				itemtile = itemtile.replace('{c}','blue');
				itemtile = itemtile.replace('{v}','');
				itemtile = itemtile.replace('{s}','wide');
				$tv.append(itemtile);
				//$tv.prepend(itemtile);

				// 7,6,5,4
				for(var j = 0; j < resp.data.length; j++){
					if(rpticon === "undefined") {
						rpticon = "news";
					}
					itemtile = htile;
					itemtile = itemtile.replace('{n}',resp.data[j].page_title);
					itemtile = itemtile.replace('{h}',resp.data[j].page);
					itemtile = itemtile.replace('{i}', this._rpticon);// 'news');
					itemtile = itemtile.replace('{c}','red');
					itemtile = itemtile.replace('{v}',resp.data[j].active_visitors.toLocaleString() + " " + "Hits");

					if(resp.data[j].active_visitors >= 1000000) {
						itemtile = itemtile.replace('{s}','large');
					} else if(resp.data[j].active_visitors >= 100000) {
						itemtile = itemtile.replace('{s}','wide');
					} else if(resp.data[j].active_visitors >= 10000) {
						itemtile = itemtile.replace('{s}','medium');
					} else {
						itemtile = itemtile.replace('{s}','medium'); //small
					}

					$tv.append(itemtile);
					//$tv.prepend(itemtile);
				}

			}, {_rpticon: rpticon})
		);
	}
});
