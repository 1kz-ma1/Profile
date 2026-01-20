
//upスタイルが画面内にきたら、スタイルupstyleを適用する
$('.up').on('inview', function() {
	$(this).addClass('upstyle');
});

//downスタイルが画面内にきたら、スタイルdownstyleを適用する
$('.down').on('inview', function() {
	$(this).addClass('downstyle');
});

//transform1スタイルが画面内にきたら、スタイルtransform1styleを適用する
$('.transform1').on('inview', function() {
	$(this).addClass('transform1style');
});

//transform2スタイルが画面内にきたら、スタイルtransform2styleを適用する
$('.transform2').on('inview', function() {
	$(this).addClass('transform2style');
});

//transform3スタイルが画面内にきたら、スタイルtransform3styleを適用する
$('.transform3').on('inview', function() {
	$(this).addClass('transform3style');
});

//blurスタイルが画面内にきたら、スタイルblurstyleを適用する
$('.blur').on('inview', function() {
	$(this).addClass('blurstyle');
});


//cont-slide
let contCurrentSlide = 0;
const contSlides = document.querySelectorAll('.cont-slide');
const contBackgrounds = [
    'url(bg1.jpg)', 'url(bg2.jpg)', 'url(bg3.jpg)'
];

function contShowSlide(index) {
    contSlides[contCurrentSlide].classList.remove('active');
    contCurrentSlide = index;
    contSlides[contCurrentSlide].classList.add('active');
    document.body.style.backgroundImage = contBackgrounds[contCurrentSlide];
}

function contNextSlide() {
    if (contCurrentSlide < contSlides.length - 1) {
    contShowSlide(contCurrentSlide + 1);
    }
}

function contPrevSlide() {
    if (contCurrentSlide > 0) {
    contShowSlide(contCurrentSlide - 1);
    }
}

function contSubmitForm() {
    const form = document.querySelector('form');
    const formData = new FormData(form);

    fetch(form.action, {
    method: 'POST',
    body: formData
    }).then(response => {
    if (response.ok) {
        window.location.href = 'thanks.html';
    } else {
        alert('送信に失敗しました');
    }
});
}

const backToTop = document.querySelector('.back-to-top');

if (backToTop) {
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
        backToTop.style.display = 'block';
        } else {
        backToTop.style.display = 'none';
        }
    });

    backToTop.addEventListener('click', (e) => {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}