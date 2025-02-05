// Reset Default Cpanel
function onCPResetDefault(_cookie){
	for (i=0;i<_cookie.length;i++) { 
		if(getCookie(TMPL_NAME+'_'+_cookie[i])!=undefined){
			createCookie (TMPL_NAME+'_'+_cookie[i], '', -1);
		}
	}
	window.location.reload(true);
}

// Apply  Cpanel
function onCPApply () {
	var elems = document.getElementById('cpanel_wrapper').getElementsByTagName ('*');
	var usersetting = {};
	
	for (i=0;i<elems.length;i++) {
		var el = elems[i]; 
	    if (el.name && (match=el.name.match(/^ytcpanel_(.*)$/))) {
	        var name = match[1];	        
	        var value = '';
	        if (el.tagName.toLowerCase() == 'input' && (el.type.toLowerCase()=='radio' || el.type.toLowerCase()=='checkbox')) {
	        	if (el.checked) value = el.value;
	        } else {
	        	value = el.value;
	        }
			if(value.trim()){
				if (usersetting[name]) {
					if (value) usersetting[name] = value + ',' + usersetting[name];
				} else {
					usersetting[name] = value;
				}
			}
	    }
	}
	
	for (var k in usersetting) {
		name = TMPL_NAME + '_' + k; 
		value = usersetting[k];
		createCookie(name, value, 365);
	}
	
	window.location.reload(true);
}


jQuery(document).ready(function($){
	
	// Select For Layout Style
	var $typeLayout = $('.typeLayout .layout-item'), $patten = $(".body-bg .pattern");
	var $body = $('#yt_wrapper');
	var ua = navigator.userAgent,
    event = (ua.match(/iPad/i)) ? "touchstart" : "click";

	// Avval saqlangan shaklni yuklash
	var savedLayout = localStorage.getItem('selectedLayout');
	if (savedLayout) {
		$typeLayout.removeClass('active'); // Barcha tugmalardan 'active' klassini olib tashlaymiz
		$typeLayout.filter('[data-value="' + savedLayout + '"]').addClass('active'); // Saqlangan shaklni faollashtiramiz
		$body.addClass(savedLayout); // Tanlangan shaklni saytga qo'llaymiz
	}

	$typeLayout.each(function(){
		var $btns = $typeLayout.bind(event, function(event) {
			var selectedLayout = $(this).data('value');

			// Yangi tanlangan shaklni saqlaymiz
			localStorage.setItem('selectedLayout', selectedLayout);

			$body
				.removeClass($btns.filter('.active').removeClass('active').data('value'))
				.addClass($(this).addClass('active').data('value'));
		});
	});

	// Reset tugmasi bosilganda default holatga qaytish
	$(".cpanel-reset a").on("click", function() {
		localStorage.removeItem('selectedLayout'); // Saqlangan shaklni o'chiramiz
		location.reload(); // Sahifani qayta yuklaymiz
	});

	/* Begin: Show hide cpanel */  
	$("#cpanel_btn").bind(event, function(event) {
		event.preventDefault();
		widthC = $('#cpanel_wrapper').width()+16;
		if ($(this).hasClass("isDown") ) {
			$("#cpanel_wrapper").animate({right:"0px"}, 400);			
			$(this).removeClass("isDown");
		} else {
			$("#cpanel_wrapper").animate({right:-widthC}, 400);	
			$(this).addClass("isDown");
		}
		return false;
	});
	/* End: Show hide cpanel */
});


jQuery(document).ready(function($) {
	// Tanlangan fon rasmini olish va saqlash
	function patternClick(elC, paramCookie, elT) {
		$(elC).click(function() {
			let oldvalue = $(this).parent().find('.active').html();
			$(elC).removeClass('active');
			$(this).addClass('active');
			let value = $(this).html();

			if (elT.length > 0) {
				for ($i = 0; $i < elT.length; $i++) {
					$(elT[$i]).removeClass(oldvalue);
					$(elT[$i]).addClass(value);
				}
			}

			// Tanlangan fonni localStoragega saqlash
			if (paramCookie) {
				$('input[name$="ytcpanel_' + paramCookie + '"]').attr('value', value);
				localStorage.setItem('selectedPattern', value); // localStoragega saqlash
			}
		});
	}

	// Pattern tanlash
	patternClick('.pattern', 'bgimage', Array('#bd'));

	// Oldingi tanlovni tiklash (localStoragedan olingan qiymat)
	let savedPattern = localStorage.getItem('selectedPattern') || 'pattern8'; // default pattern
	$('.pattern').each(function() {
		if ($(this).data('pattern') === savedPattern) {
			$(this).addClass('active');
			$('#bd').removeClass().addClass(savedPattern); // Bodyga tanlangan klassni qo'shish
		}
	});

	/* Cpanel funktsiyasi */
	function setCpanelValues(array) {
		if (array['0']) {
			$('.body-backgroud-image .pattern').removeClass('active');
			$('.body-backgroud-image .pattern.' + array['3']).addClass('active');
			$('input[name$="ytcpanel_bgimage"]').attr('value', array['3']);
		}
	}

	// Boshlang'ich pattern
	let array_default = Array('pattern8');
	setCpanelValues(array_default);
});


document.addEventListener("DOMContentLoaded", function () {
    // LocalStorage dan saqlangan ma'lumotlarni olish
    let savedBackground = localStorage.getItem("background");
    let savedColor = localStorage.getItem("color");
    let savedFontSize = localStorage.getItem("fontSize");
    let savedFilter = localStorage.getItem("filter");

    // Agar oldin saqlangan bo'lsa, sahifaga qo'llash
    if (savedBackground) document.body.style.backgroundColor = savedBackground;
    if (savedColor) document.body.style.color = savedColor;
    if (savedFontSize) document.body.style.fontSize = savedFontSize + "px";
    if (savedFilter) document.body.style.filter = savedFilter;

    let defaultFontSize = 13; // Asl shrift o‘lchami
    let currentFontSize = savedFontSize ? parseInt(savedFontSize) : defaultFontSize;

    function changeFontSize(size) {
        document.body.style.fontSize = size + "px";
        localStorage.setItem("fontSize", size); // Shriftni saqlash
    }

    // FON SOZLAMALARI

    document.getElementById("toggle-black-white").addEventListener("click", function (event) {
        event.preventDefault();
        document.body.style.filter = "grayscale(100%)"; // Oq-qora qilish
        document.body.style.backgroundColor = "#fff"; // Oq fon
        document.body.style.color = "#000"; // Qora matn
        localStorage.setItem("background", "#fff");
        localStorage.setItem("color", "#000");
        localStorage.setItem("filter", "grayscale(100%)");
    });

    document.getElementById("toggle-yellow-black").addEventListener("click", function (event) {
        event.preventDefault();
        document.body.style.backgroundColor = "#d48429"; // Sariq fon
        document.body.style.color = "#8B0000"; // Qizil rang matn
        document.body.style.filter = "none"; // Filterni olib tashlash
        localStorage.setItem("background", "#FFD700");
        localStorage.setItem("color", "#8B0000");
        localStorage.setItem("filter", "none");
    });

    // **DEFAULT HOLATGA QAYTARISH**
    document.getElementById("toggle-original").addEventListener("click", function (event) {
        event.preventDefault();
        document.body.style.filter = "none"; // Asl rangga qaytarish
        document.body.style.backgroundColor = ""; // Default fon
        document.body.style.color = ""; // Default matn
        document.body.style.fontSize = defaultFontSize + "px"; // Asl shrift hajmi
        localStorage.removeItem("background");
        localStorage.removeItem("color");
        localStorage.removeItem("filter");
        localStorage.setItem("fontSize", defaultFontSize); // Default shriftni saqlash
    });

    // SHRIFT SOZLAMALARI

    document.getElementById("small-text").addEventListener("click", function (event) {
        event.preventDefault();
        currentFontSize -= 1; // 1px ga kamaytirish
        changeFontSize(currentFontSize);
    });

    document.getElementById("normal-text").addEventListener("click", function (event) {
        event.preventDefault();
        currentFontSize = defaultFontSize; // Default holat
        changeFontSize(currentFontSize);
    });

    document.getElementById("large-text").addEventListener("click", function (event) {
        event.preventDefault();
        currentFontSize += 1; // 1px ga oshirish
        changeFontSize(currentFontSize);
    });
});
