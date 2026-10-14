'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

(function ($) {
    var OpalThemeBacktop = function () {
        function OpalThemeBacktop() {
            _classCallCheck(this, OpalThemeBacktop);

            this.initBacktotop();
        }

        _createClass(OpalThemeBacktop, [{
            key: 'initBacktotop',
            value: function initBacktotop() {
                jQuery(window).scroll(function () {
                    if (jQuery(this).scrollTop() > 200) {
                        jQuery('.scrollup').fadeIn().addClass('activate');
                    } else {
                        jQuery('.scrollup').fadeOut().removeClass('activate');
                    }
                });
                jQuery('.scrollup').on('click', function () {
                    jQuery("html, body").animate({ scrollTop: 0 }, 600);
                    return false;
                });
            }
        }]);

        return OpalThemeBacktop;
    }();

    new OpalThemeBacktop();
    jQuery('html').removeClass('no-js').addClass('js yes-js js_active');

    var OpalThemeFooter = function () {
        function OpalThemeFooter() {
            _classCallCheck(this, OpalThemeFooter);

            this.init();
        }

        _createClass(OpalThemeFooter, [{
            key: 'init',
            value: function init() {
                var _this = this;

                if (jQuery('body').hasClass('footer-fixed')) {
                    this.$footer = jQuery('#colophon');
                    this.$content = jQuery('#page');
                    this.$footer.css({
                        position: 'fixed',
                        left: 0,
                        bottom: 0,
                        zIndex: 0
                    });

                    this.setup();

                    $(window).resize(function () {
                        _this.setup();
                    });
                }
            }
        }, {
            key: 'setup',
            value: function setup() {
                this.$content.css({
                    marginBottom: this.getFooterHeight()
                });
            }
        }, {
            key: 'getFooterHeight',
            value: function getFooterHeight() {
                return this.$footer.outerHeight();
            }
        }]);

        return OpalThemeFooter;
    }();

    new OpalThemeFooter();

    var OpalThemeLogin = function () {
        function OpalThemeLogin() {
            _classCallCheck(this, OpalThemeLogin);

            jQuery('body').on('click', '.opal-login-form-ajax button[type="submit"]', function (event) {
                var $this = $(event.currentTarget);
                var $form = $this.closest('form');

                $.ajax({
                    type: 'POST',
                    url: osfAjax.ajaxurl,
                    data: $form.serialize(),
                    beforeSend: function beforeSend() {
                        $form.addClass('loading');
                        // $form.find('.woocommerce-error').remove();
                        $form.find('input,button').prop('disabled', true);
                    },
                    success: function success(response) {
                        if (response.status) {
                            location.reload();
                        } else {
                            // $form.before(`<div class="woocommerce-error">${response.msg}</div>`);
                        }
                    },
                    complete: function complete() {
                        $form.find('input,button').prop('disabled', false);
                        $form.removeClass('loading');
                    }
                });

                return false;
            });
        }

        _createClass(OpalThemeLogin, [{
            key: 'beforeSend',
            value: function beforeSend() {}
        }]);

        return OpalThemeLogin;
    }();

    new OpalThemeLogin();

    var OpalTheme_Main_Menu = function () {
        function OpalTheme_Main_Menu() {
            _classCallCheck(this, OpalTheme_Main_Menu);

            this.initSubmenuHover();
        }

        _createClass(OpalTheme_Main_Menu, [{
            key: 'initSubmenuHover',
            value: function initSubmenuHover() {
                var _this2 = this;

                $('.site-header .main-navigation .menu-item-has-children').hover(function (event) {
                    var $item = $(event.currentTarget);
                    _this2.setPositionLvN($item);
                });
            }
        }, {
            key: 'setPositionLvN',
            value: function setPositionLvN($item) {
                var sub = $item.children('.sub-menu'),
                    offset = $item.offset(),
                    width = $item.outerWidth(),
                    screen_width = $(window).width(),
                    sub_width = sub.outerWidth();
                var align_delta = offset.left + width + sub_width - screen_width;
                if (align_delta >= 0) {
                    sub.css({ left: 'auto', right: '100%' });
                } else {
                    sub.css({ left: '', right: '' });
                }
            }
        }]);

        return OpalTheme_Main_Menu;
    }();

    new OpalTheme_Main_Menu();

    var OpalThemeOwlCarousel = function OpalThemeOwlCarousel() {
        _classCallCheck(this, OpalThemeOwlCarousel);
    };

    new OpalThemeOwlCarousel();

    var OpalThemeSmoothMenu = function () {
        function OpalThemeSmoothMenu() {
            var _this3 = this;

            _classCallCheck(this, OpalThemeSmoothMenu);

            fundorJS.smoothCallback = function (selector) {
                jQuery('.opal-smooth-menu a[href^="' + selector + '"]').trigger('click');
            };

            jQuery('body').on('click', '.opal-smooth-menu a[href^="#"]', function (e) {
                e.preventDefault();
                _this3.menuActiveClass(e);
                var target = e.currentTarget.hash;
                var $target = $(target);
                if ($target.length > 0) {
                    jQuery('html, body').animate({
                        'scrollTop': $target.offset().top - _this3.getOffset()
                    }, 600, 'swing');
                }
            });
        }

        _createClass(OpalThemeSmoothMenu, [{
            key: 'menuActiveClass',
            value: function menuActiveClass(e) {
                var $this = $(e.currentTarget);
                jQuery('.opal-smooth-menu').find('li.menu-item').removeClass('current-menu-item current_page_item');
                var selector = $this.closest('li').attr('id');
                jQuery('.opal-smooth-menu [id="' + selector + '"]').addClass('current-menu-item');
            }
        }, {
            key: 'getOffset',
            value: function getOffset() {
                var offset = 0;
                var $adminBar = jQuery('#wpadminbar');
                var $stickyHeader = jQuery('#opal-header-sticky');

                if ($adminBar.length > 0) {
                    offset += $adminBar.outerHeight();
                }

                if ($stickyHeader.length > 0) {
                    offset += $stickyHeader.outerHeight();
                }

                return offset;
            }
        }]);

        return OpalThemeSmoothMenu;
    }();

    new OpalThemeSmoothMenu();

    var OpalThemeStickyHeader = function () {
        function OpalThemeStickyHeader() {
            _classCallCheck(this, OpalThemeStickyHeader);

            this.sticky();
        }

        _createClass(OpalThemeStickyHeader, [{
            key: 'sticky',
            value: function sticky() {
                var $scope = $('#opal-header-content');
                if ($scope.length > 0) {
                    var section_offset = $scope.offset().top,
                        section_top = $('#wpadminbar').height(),
                        section_height = $scope.outerHeight();
                    if ($(window).width() < 601) {
                        section_top = 0;
                    }
                    $(window).resize(function () {
                        $scope.removeClass('sticky-show');
                        $scope.css({
                            top: 0
                        });
                        var $h_animate = $scope.next('.h-animate');
                        $h_animate.remove();
                        if (!$scope.hasClass('sticky-show')) {
                            section_offset = $scope.offset().top;
                        }
                        section_top = $('#wpadminbar').height();
                        if ($(window).width() < 601) {
                            section_top = 0;
                        }
                    });
                    $(window).scroll(function () {
                        if ($(window).width() > 768) {
                            if ($(window).scrollTop() >= section_offset + section_height - section_top) {
                                if (!$scope.hasClass('sticky-show')) {
                                    $scope.addClass('sticky-show');
                                    $scope.css({
                                        top: section_top
                                    });
                                    $("<div class='h-animate'></div>").insertAfter($scope).css({
                                        height: section_height
                                    });
                                }
                            } else {
                                $scope.removeClass('sticky-show');
                                $scope.css({
                                    top: 0
                                });
                                var $h_animate = $scope.next('.h-animate');
                                $h_animate.remove();
                            }
                        }
                    });
                }
            }
        }]);

        return OpalThemeStickyHeader;
    }();

    jQuery(document).ready(function ($) {
        new OpalThemeStickyHeader();
    });

    var OpalTheme = function () {
        function OpalTheme() {
            var _this4 = this;

            _classCallCheck(this, OpalTheme);

            this.SetUpBreacumb();
            jQuery(window).resize(function () {
                _this4.SetUpBreacumb();
            });

            $(window).load(function () {
                _this4.initBG();
            });
        }

        _createClass(OpalTheme, [{
            key: 'SetUpBreacumb',
            value: function SetUpBreacumb() {

                var header = jQuery('body.opal-header-absolute #masthead .site-header'),
                    breacumb = jQuery('.page-title-bar .wrap');
                if (header.length) {

                    if (jQuery(window).width() > 992) {
                        var Height = header.height(),
                            breacumbHeight = breacumb.height();
                        breacumb.css({
                            'min-height': breacumbHeight + Height,
                            'padding-top': Height
                        });
                    } else {
                        breacumb.css({
                            'min-height': '',
                            'padding-top': ''
                        });
                    }
                }
            }
        }, {
            key: 'initBG',
            value: function initBG() {
                var _this5 = this;

                if ($('.body-background-inner').length > 0) {
                    this.bgScale();
                    $(document).on('scroll', function () {
                        _this5.bgScale();
                    });
                }
            }
        }, {
            key: 'bgScale',
            value: function bgScale() {
                var documentHeight = $(document).height() - $(window).height();
                var _h = window.pageYOffset;
                var scale = 1 + _h / documentHeight / 4;

                $('.body-background-inner').css({
                    "transform": 'translate(-50%, -50%) scale(' + scale + ')'
                });
            }
        }]);

        return OpalTheme;
    }();

    jQuery(document).ready(function ($) {
        new OpalTheme();
    });

    var OpalThemeToogle = function () {
        function OpalThemeToogle() {
            _classCallCheck(this, OpalThemeToogle);

            this.setupHeader();
            this.toggleCollapse();
            this.ToggleCanvasFilter();
            this.PositionAccount();
            this.toggleCollapseSearchFooter();
        }

        _createClass(OpalThemeToogle, [{
            key: 'setupHeader',
            value: function setupHeader() {
                jQuery('#masthead .search-button[data-search-toggle]').each(function (index, element) {
                    var $button = $(element);
                    if ($button.hasClass('top-to-bottom') || $button.hasClass('popup')) {
                        var $searchform = $($button.data('target'));
                        $searchform.data('height', $searchform.outerHeight()).prependTo('#page').addClass('loaded');
                    } else if ($button.hasClass('bottom-to-top')) {
                        var _$searchform = $($button.data('target'));
                        _$searchform.data('height', _$searchform.outerHeight()).prependTo('#page');
                    }
                });
            }
        }, {
            key: 'toggleCollapse',
            value: function toggleCollapse() {
                var _this6 = this;

                jQuery('body').on('click', '[data-search-toggle="toggle"]', function (e) {
                    e.preventDefault();
                    var $button = $(e.currentTarget);
                    var $searchForm = $($button.data('target'));
                    var $buttonClose = $searchForm.find('[data-search-toggle="close"]');
                    $buttonClose.on('click', function (e) {
                        $button.removeClass('active');
                        $searchForm.removeClass('active');
                        jQuery('body').removeClass('over-hidden');
                        if ($buttonClose.closest('.bottom-to-top')) {
                            $searchForm.css('top', '100%');
                        }
                    });
                    if ($button.is('.top-to-bottom, .bottom-to-top, .popup')) {
                        $searchForm.toggleClass('active');
                        $button.toggleClass('active');
                    }
                    if ($button.hasClass('top-to-bottom')) {
                        _this6.setupTopToBottom($button, $searchForm);
                    } else if ($button.hasClass('bottom-to-top')) {
                        _this6.setupBottomToTop($button, $searchForm);
                    } else if ($button.hasClass('popup')) {
                        _this6.setupFullScreen($button, $searchForm);
                    } else {
                        $button.toggleClass('active');
                        $button.siblings($searchForm).toggleClass('active');
                        $(document.createElement('div')).addClass('dropdown-backdrop').insertAfter($button.siblings($searchForm)).on('click', function () {
                            jQuery(this).siblings().removeClass("active");
                            jQuery(this).remove();
                        });
                    }
                });
            }
        }, {
            key: 'toggleCollapseSearchFooter',
            value: function toggleCollapseSearchFooter() {
                jQuery('body').on('click', '.search-footer', function (e) {
                    e.preventDefault();
                    $('.handheld-footer-bar .search').toggleClass('active');
                });
            }
        }, {
            key: 'checkScroll',
            value: function checkScroll($object) {
                var element = $object.get(0);
                return element.scrollHeight > $(window).height();
            }
        }, {
            key: 'setupFullScreen',
            value: function setupFullScreen($button, $searchForm) {
                var $body = jQuery('body');
                if (this.checkScroll($body)) {
                    $body.toggleClass('over-hidden');
                }
            }
        }, {
            key: 'setupTopToBottom',
            value: function setupTopToBottom($button, $searchForm) {
                jQuery('body').animate({ scrollTop: 0 }, 600);
            }
        }, {
            key: 'setupBottomToTop',
            value: function setupBottomToTop($button, $searchForm) {
                var $header = jQuery('.site-header'),
                    $sticky = jQuery('.sticky-show'),
                    stickyHeight = $sticky.outerHeight(),
                    adminbarHeight = jQuery('#wpadminbar').height(),
                    position = $header.height() + adminbarHeight;
                if (stickyHeight > 1) {
                    position = stickyHeight + adminbarHeight;
                }
                if ($searchForm.hasClass('active')) {
                    $searchForm.css('top', position);
                } else {
                    $searchForm.css('top', '100%');
                }
                var $body = $('body');
                if (this.checkScroll($body)) {
                    $body.toggleClass('over-hidden');
                }
            }
        }, {
            key: 'ToggleCanvasFilter',
            value: function ToggleCanvasFilter() {
                jQuery('body').on('click', '.opal-overlay-filter , .filter-close', function () {
                    jQuery('body').removeClass('opal-canvas-filter-open');
                    jQuery('.filter-toggle').removeClass('active');
                }).on('click', '.filter-toggle', function (event) {
                    var $body = jQuery('body');
                    var filterToggle = $(event.currentTarget);
                    if ($body.hasClass('opal-canvas-filter-open')) {
                        filterToggle.removeClass('active');
                        $body.removeClass('opal-canvas-filter-open');
                        $body.find('.opal-canvas-filter.top').slideToggle(1000);
                    } else {
                        filterToggle.addClass('active');
                        $body.addClass('opal-canvas-filter-open');
                        $body.find('.opal-canvas-filter.top').slideToggle(1000);
                    }
                });
            }
        }, {
            key: 'PositionAccount',
            value: function PositionAccount() {
                jQuery('body').on('hover', '.site-header-account', function () {
                    var $drop = jQuery(this).find('.account-dropdown');
                    if ($drop.length > 0) {
                        var position = $drop.offset().top - $(window).scrollTop() + $drop.outerHeight(true),
                            top = position - jQuery(window).height();
                        if (top > 0) {
                            $drop.css({
                                'transform': 'translateY( -' + top + 'px)'
                            });
                        }
                    }
                });
            }
        }]);

        return OpalThemeToogle;
    }();

    jQuery(document).ready(function ($) {
        new OpalThemeToogle();
    });
})(jQuery);
//# sourceMappingURL=theme.js.map
