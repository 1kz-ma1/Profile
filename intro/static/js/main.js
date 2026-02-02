
//===============================================================
// debounce関数
//===============================================================
// デバッグログ: main.js が読み込まれたかと jQuery の存在確認
try {
    console.log('main.js loaded');
    if (window.jQuery) {
        console.log('jQuery version:', jQuery.fn && jQuery.fn.jquery ? jQuery.fn.jquery : '(unknown)');
    } else {
        console.log('jQuery is NOT available');
    }
} catch (e) {
    // コンソールがない環境での保険
}

function debounce(func, wait) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
            timeout = null;
            func.apply(context, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}


//===============================================================
// メニュー関連
//===============================================================

// 変数でセレクタを管理
var $menubar = $('#menubar');
var $menubarHdr = $('#menubar_hdr');

// menu
$(window).on("load resize", debounce(function() {
    console.log('resize event fired, width:', window.innerWidth);
    if(window.innerWidth < 900) {	// ここがブレイクポイント指定箇所です
        // 小さな端末用の処理
        console.log('mobile mode');
        $('body').addClass('small-screen').removeClass('large-screen');
        $menubar.addClass('display-none').removeClass('display-block');
        $menubarHdr.removeClass('display-none ham').addClass('display-block');
    } else {
        // 大きな端末用の処理
        console.log('desktop mode');
        $('body').addClass('large-screen').removeClass('small-screen');
        $menubar.addClass('display-block').removeClass('display-none');
        $menubarHdr.removeClass('display-block').addClass('display-none');

        // ドロップダウンメニューが開いていれば、それを閉じる
        $('.ddmenu_parent > ul').hide();
    }
}, 10));

$(function() {

    // ハンバーガーメニューをクリックした際の処理
    $menubarHdr.click(function() {
        $(this).toggleClass('ham');
        if ($(this).hasClass('ham')) {
            $menubar.addClass('display-block');
            $('#overlay').removeClass('display-none').addClass('display-block');
            // ボディのスクロールをロック
            $('body').css({
                'overflow': 'hidden',
                'position': 'fixed',
                'width': '100%'
            });
        } else {
            $menubar.removeClass('display-block');
            $('#overlay').removeClass('display-block').addClass('display-none');
            // ボディのスクロールロックを解除
            $('body').css({
                'overflow': '',
                'position': '',
                'width': ''
            });
        }
    });

    // アンカーリンクの場合にメニューを閉じる処理
    $menubar.find('a[href*="#"]').click(function() {
        $menubar.removeClass('display-block');
        $menubarHdr.removeClass('ham');
        $('#overlay').removeClass('display-block').addClass('display-none');
        // スクロールロック解除
        $('body').css({
            'overflow': '',
            'position': '',
            'width': ''
        });
    });

    // 通常のページリンク（ナビゲーション内）をクリックした時、メニューを閉じる
    $menubar.find('a:not([href*="#"]):not([href=""])').click(function(e) {
        // メニューを即座に非表示にする
        $menubar.removeClass('display-block').addClass('display-none');
        $menubarHdr.removeClass('ham');
        $('#overlay').removeClass('display-block').addClass('display-none');
        // スクロールロック解除
        $('body').css({
            'overflow': '',
            'position': '',
            'width': ''
        });
        // デフォルト動作を継続させてページ遷移を許可
        return true;
    });

    // ドロップダウンの親liタグ（空のリンクを持つaタグのデフォルト動作を防止）
	$menubar.find('a[href=""]').click(function() {
		return false;
	});

	// ドロップダウンメニューの処理
    $menubar.find('li:has(ul)').addClass('ddmenu_parent');
    $('.ddmenu_parent > a').addClass('ddmenu');

// タッチ開始位置を格納する変数
var touchStartY = 0;

// タッチデバイス用
$('.ddmenu').on('touchstart', function(e) {
    // タッチ開始位置を記録
    touchStartY = e.originalEvent.touches[0].clientY;
}).on('touchend', function(e) {
    // タッチ終了時の位置を取得
    var touchEndY = e.originalEvent.changedTouches[0].clientY;
    
    // タッチ開始位置とタッチ終了位置の差分を計算
    var touchDifference = touchStartY - touchEndY;
    
    // スクロール動作でない（差分が小さい）場合にのみドロップダウンを制御
    if (Math.abs(touchDifference) < 10) { // 10px以下の移動ならタップとみなす
        var $nextUl = $(this).next('ul');
        if ($nextUl.is(':visible')) {
            $nextUl.stop().hide();
        } else {
            $nextUl.stop().show();
        }
        $('.ddmenu').not(this).next('ul').hide();
        return false; // ドロップダウンのリンクがフォローされるのを防ぐ
    }
});

// オーバーレイをクリックしたらメニューを閉じる
$(function() {
    $('#overlay').click(function() {
        $('#menubar').removeClass('display-block');
        $('#menubar_hdr').removeClass('ham');
        $(this).removeClass('display-block').addClass('display-none');
        // スクロールロック解除
        $('body').css({
            'overflow': '',
            'position': '',
            'width': ''
        });
    });

    // リサイズ時に overlay が残らないようにする
    $(window).on('resize', debounce(function() {
        if (window.innerWidth >= 900) {
            $('#overlay').removeClass('display-block').addClass('display-none');
            $('#menubar_hdr').removeClass('ham');
            // スクロールロック解除
            $('body').css({
                'overflow': '',
                'position': '',
                'width': ''
            });
        }
    }, 100));
});

    //PC用
    $('.ddmenu_parent').hover(function() {
        $(this).children('ul').stop().show();
    }, function() {
        $(this).children('ul').stop().hide();
    });

    // ドロップダウンをページ内リンクで使った場合に、ドロップダウンを閉じる
    $('.ddmenu_parent ul a').click(function() {
        $('.ddmenu_parent > ul').hide();
    });

});


//===============================================================
// 小さなメニューが開いている際のみ、body要素のスクロールを禁止。
//===============================================================
$(function() {
    function toggleBodyScroll() {
    // 条件をチェック
    if ($('#menubar_hdr').hasClass('ham') && !$('#menubar_hdr').hasClass('display-none')) {
      // #menubar_hdr が 'ham' クラスを持ち、かつ 'display-none' クラスを持たない場合、スクロールを禁止
        $('body').css({
        overflow: 'hidden',
        height: '100%'
        });
    } else {
      // その他の場合、スクロールを再び可能に
        $('body').css({
        overflow: '',
        height: ''
        });
    }
}

  // 初期ロード時にチェックを実行
    toggleBodyScroll();

  // クラスが動的に変更されることを想定して、MutationObserverを使用
    const observer = new MutationObserver(toggleBodyScroll);
    observer.observe(document.getElementById('menubar_hdr'), { attributes: true, attributeFilter: ['class'] });
});


//===============================================================
// スムーススクロール（※バージョン2024-1）※ヘッダーの高さとマージンを取得する場合
//===============================================================
$(function() {
    var headerHeight = $('header').outerHeight();
    var headerMargin = parseInt($('header').css("margin-top"));
    var totalHeaderHeight = headerHeight + headerMargin;
    // ページ上部へ戻るボタンのセレクター
    var topButton = $('.pagetop');
    // ページトップボタン表示用のクラス名
    var scrollShow = 'pagetop-show';

    // スムーススクロールを実行する関数
    // targetにはスクロール先の要素のセレクターまたは'#'（ページトップ）を指定
    function smoothScroll(target) {
        // スクロール先の位置を計算（ページトップの場合は0、それ以外は要素の位置）
        var scrollTo = target === '#' ? 0 : $(target).offset().top - totalHeaderHeight;
        // アニメーションでスムーススクロールを実行
        $('html, body').animate({scrollTop: scrollTo}, 500);
    }

    // ページ内リンクとページトップへ戻るボタンにクリックイベントを設定
    $('a[href^="#"], .pagetop').click(function(e) {
        e.preventDefault(); // デフォルトのアンカー動作をキャンセル
        var id = $(this).attr('href') || '#'; // クリックされた要素のhref属性を取得、なければ'#'
        smoothScroll(id); // スムーススクロールを実行
    });

    // スクロールに応じてページトップボタンの表示/非表示を切り替え
    $(topButton).hide(); // 初期状態ではボタンを隠す
    $(window).scroll(function() {
        if($(this).scrollTop() >= 300) { // スクロール位置が300pxを超えたら
            $(topButton).fadeIn().addClass(scrollShow); // ボタンを表示
        } else {
            $(topButton).fadeOut().removeClass(scrollShow); // それ以外では非表示
        }
    });

    // ページロード時にURLのハッシュが存在する場合の処理
    if(window.location.hash) {
        // ページの最上部に即時スクロールする
        $('html, body').scrollTop(0);
        // 少し遅延させてからスムーススクロールを実行
        setTimeout(function() {
            smoothScroll(window.location.hash);
        }, 10);
    }
});


//===============================================================
// 汎用開閉処理
//===============================================================
$(function() {
	$('.openclose-parts').next().hide();
	$('.openclose-parts').click(function() {
		$(this).next().slideToggle();
		$('.openclose-parts').not(this).next().slideUp();
	});
});


//===============================================================
// テキストのフェードイン効果
//===============================================================
$(function() {
    $('.fade-in-text').on('inview', function(event, isInView) {
        // この要素が既にアニメーションされたかどうかを確認
        if (isInView && !$(this).data('animated')) {
            // アニメーションがまだ実行されていない場合
            let innerHTML = '';
            const text = $(this).text();
            $(this).text('');

            for (let i = 0; i < text.length; i++) {
                innerHTML += `<span class="char" style="animation-delay: ${i * 0.2}s;">${text[i]}</span>`;
            }

            $(this).html(innerHTML).css('visibility', 'visible');
            // アニメーションが実行されたことをマーク
            $(this).data('animated', true);
        }
    });
});


//===============================================================
// 詳細ページのサムネイル切り替え
//===============================================================
$(function() {
    // 初期表示: 各 .thumbnail-view に対して、直後の .thumbnail の最初の画像を表示
    $(".thumbnail-view-parts").each(function() {
        var firstThumbnailSrc = $(this).next(".thumbnail-parts").find("img:first").attr("src");
        var defaultImage = $("<img>").attr("src", firstThumbnailSrc);
        $(this).append(defaultImage);
    });

    // サムネイルがクリックされたときの動作
    $(".thumbnail-parts img").click(function() {
        var imgSrc = $(this).attr("src");
        var newImage = $("<img>").attr("src", imgSrc).hide();

        // このサムネイルの直前の .thumbnail-view 要素を取得
        var targetPhoto = $(this).parent(".thumbnail-parts").prev(".thumbnail-view-parts");

        targetPhoto.find("img").fadeOut(400, function() {
            targetPhoto.empty().append(newImage);
            newImage.fadeIn(400);
        });
    });
});


//===============================================================
// スライドショー
//===============================================================
const slides = document.querySelectorAll('.slide');
let currentIndex = 0;
let slideInterval;

function showSlide(index) {
  slides.forEach((slide, i) => {
    slide.style.opacity = i === index ? '1' : '0';
    slide.classList.toggle('active', i === index);
  });
}

function nextSlide() {
  currentIndex = (currentIndex + 1) % slides.length;
  showSlide(currentIndex);
}

function prevSlide() {
  currentIndex = (currentIndex - 1 + slides.length) % slides.length;
  showSlide(currentIndex);
}

function startAutoSlide() {
  slideInterval = setInterval(nextSlide, 3500);
}

function resetAutoSlide() {
  clearInterval(slideInterval);
  startAutoSlide();
}

// ===== スワイプ操作（左右のみ） =====
const sliderRoot = document.getElementById('mainimg');
if (sliderRoot) {  // スライドショーが存在する場合のみ実行
const swipeTarget = sliderRoot;
let startX = 0, startY = 0, dragging = false, startTime = 0, pointerId = null;
const SWIPE_THRESHOLD = 40;  // 最低移動量(px)
const SWIPE_MAX_TIME  = 700; // 最大判定時間(ms)

function onSwipeStart(x, y) {
  startX = x; startY = y;
  startTime = performance.now();
  dragging = true;
  swipeTarget.classList.add('is-dragging');
}

function onSwipeMove(x, y, preventDefault) {
  if (!dragging) return;
  const dx = x - startX, dy = y - startY;
  if (Math.abs(dx) > Math.abs(dy)) preventDefault(); // 横優先時のみ縦スクロール抑制
}

function onSwipeEnd(x, y) {
  if (!dragging) return;
  const dx = x - startX, dy = y - startY, dt = performance.now() - startTime;
  dragging = false;
  swipeTarget.classList.remove('is-dragging');

  if (Math.abs(dx) > SWIPE_THRESHOLD && Math.abs(dx) > Math.abs(dy) && dt < SWIPE_MAX_TIME) {
    if (dx < 0) nextSlide(); else prevSlide();
    resetAutoSlide();
  }
}

// Pointer Events 優先
if (window.PointerEvent) {
  swipeTarget.addEventListener('pointerdown', (e) => {
    pointerId = e.pointerId;
    onSwipeStart(e.clientX, e.clientY);
    swipeTarget.setPointerCapture?.(pointerId);
  }, { passive: true });

  swipeTarget.addEventListener('pointermove', (e) => {
    onSwipeMove(e.clientX, e.clientY, () => e.preventDefault());
  }, { passive: false });

  const endPointer = (e) => {
    onSwipeEnd(e.clientX ?? startX, e.clientY ?? startY); // ← 終了時の座標を使うと判定が素直
    swipeTarget.releasePointerCapture?.(pointerId);
    pointerId = null;
  };
  swipeTarget.addEventListener('pointerup', endPointer, { passive: true });
  swipeTarget.addEventListener('pointercancel', endPointer, { passive: true });
  swipeTarget.addEventListener('pointerleave', endPointer, { passive: true });
} else {
  // Touch フォールバック
  swipeTarget.addEventListener('touchstart', (e) => {
    const t = e.changedTouches[0];
    onSwipeStart(t.clientX, t.clientY);
  }, { passive: true });

  swipeTarget.addEventListener('touchmove', (e) => {
    const t = e.changedTouches[0];
    onSwipeMove(t.clientX, t.clientY, () => e.preventDefault());
  }, { passive: false });

  const endTouch = (e) => {
    const t = e.changedTouches[0];
    onSwipeEnd(t.clientX, t.clientY);
  };
  swipeTarget.addEventListener('touchend', endTouch, { passive: true });
  swipeTarget.addEventListener('touchcancel', endTouch, { passive: true });
}
sliderRoot.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') { prevSlide(); resetAutoSlide(); }
    if (e.key === 'ArrowRight'){ nextSlide(); resetAutoSlide(); }
});
// 初期表示（この順序が安全）
showSlide(currentIndex);
startAutoSlide();
}  // if (sliderRoot) の閉じ括弧


/*最新情報ページング*/

const items = document.querySelectorAll('.news-list li');
const itemsPerPage = 4;
let currentPage = 1;

function showPage(page) {
    items.forEach((item, index) => {
        item.style.display = (index >= (page - 1) * itemsPerPage && index < page * itemsPerPage) ? 'block' : 'none';
    });

    // ページ番号のアクティブ状態を更新
    document.querySelectorAll('#pagination button.page-btn').forEach((btn, idx) => {
        btn.classList.toggle('active', idx + 1 === page);
    });
}

function setupPagination() {
    const pageNumbers = document.getElementById('page-numbers');
    if (!pageNumbers) return;
    
    const totalPages = Math.ceil(items.length / itemsPerPage);
    pageNumbers.innerHTML = '';

    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement('button');
        btn.textContent = i;
        btn.classList.add('page-btn');
        btn.addEventListener('click', () => {
            currentPage = i;
            showPage(currentPage);
        });
        pageNumbers.appendChild(btn);
    }
}

const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');

if (prevBtn) {
    prevBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            showPage(currentPage);
        }
    });
}

if (nextBtn) {
    nextBtn.addEventListener('click', () => {
        if (currentPage < Math.ceil(items.length / itemsPerPage)) {
            currentPage++;
            showPage(currentPage);
        }
    });
}

setupPagination();
showPage(currentPage);
``

const newsList = document.querySelector('.news-list');
const sortButton = document.getElementById('sort-toggle');
let sortDescending = true; // 初期状態：新しい順

if (sortButton && newsList) {
    sortButton.addEventListener('click', () => {
        
    const itemsArray = Array.from(newsList.querySelectorAll('li'));

itemsArray.sort((a, b) => {
    const dateA = parseDate(a.querySelector('.news-title').textContent);
    const dateB = parseDate(b.querySelector('.news-title').textContent);
    return sortDescending ? dateB - dateA : dateA - dateB;
});

function parseDate(text) {
    const match = text.match(/＜(.*?)＞/);
    if (!match) return new Date(0);
    const rawDate = match[1].replace(/[年月]/g, '-').replace(/日/, '');
    return new Date(rawDate); // "2025-10-21" → OK
}

    // 並び替えた要素を再描画
    itemsArray.forEach(item => newsList.appendChild(item));

    // ページネーションを再適用
    setupPagination();
    showPage(1);

        // ボタンの表示を切り替え
        sortDescending = !sortDescending;
        sortButton.textContent = sortDescending ? '日付：降順' : '日付：昇順';
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const img = document.querySelector(".profile-img");
    if (img) {
        setTimeout(() => {
        img.classList.add("show");
        }, 500);
    }
});

