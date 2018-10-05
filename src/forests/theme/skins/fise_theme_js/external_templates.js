// Native Javascript for Bootstrap 3 v2.0.24 | © dnp_theme | MIT-License
!function(t,e){if("function"==typeof define&&define.amd)define([],e);else if("object"==typeof module&&module.exports)module.exports=e();else{var n=e();t.Collapse=n.Collapse}}(this,function(){"use strict";var t="undefined"!=typeof global?global:this||window,e=document,n=e.documentElement,i=t.BSN={},o=i.supports=[],a="Transition",l="Webkit",s="style",r=(n[s],l+a in n[s]||a.toLowerCase()in n[s]),c=l+a in n[s]?l.toLowerCase()+a+"End":a.toLowerCase()+"end",u=l+"Duration"in n[s]?l.toLowerCase()+a+"Duration":a.toLowerCase()+"Duration",f=function(t,e){t.classList.add(e)},d=function(t,e){t.classList.remove(e)},p=function(t,e){return t.classList.contains(e)},g=function(t,n){var i=n||e;return"object"==typeof t?t:i.querySelector(t)},h=function(t,n){var i=n.charAt(0),o=n.substr(1);if("."===i){for(;t&&t!==e;t=t.parentNode)if(null!==g(n,t.parentNode)&&p(t,o))return t}else if("#"===i)for(;t&&t!==e;t=t.parentNode)if(t.id===o)return t;return!1},m=function(t,e,n){t.addEventListener(e,n,!1)},v=function(t,e,n){t.removeEventListener(e,n,!1)},A=function(t,e,n){m(t,e,function i(o){n(o),v(t,e,i)})},b=function(e){var n=t.getComputedStyle(e)[u];return n=parseFloat(n),(n="number"!=typeof n||isNaN(n)?0:1e3*n)+50},C=function(t,e){var n=0,i=b(t);r&&A(t,c,function(t){e(t),n=1}),setTimeout(function(){!n&&e()},i)},w=function(t,e,n){var i=new CustomEvent(t+".bs."+e);i.relatedTarget=n,this.dispatchEvent(i)};i.version="2.0.24";var L=function(t,e){t=g(t),e=e||{};var n,i,o=null,a=null,l=this,r=t.getAttribute("data-parent"),c=function(t,e){w.call(t,"show","collapse"),t.isAnimating=!0,f(t,"collapsing"),d(t,"collapse"),t[s].height=t.scrollHeight+"px",C(t,function(){t.isAnimating=!1,t.setAttribute("aria-expanded","true"),e.setAttribute("aria-expanded","true"),d(t,"collapsing"),f(t,"collapse"),f(t,"in"),t[s].height="",w.call(t,"shown","collapse")})},u=function(t,e){w.call(t,"hide","collapse"),t.isAnimating=!0,t[s].height=t.scrollHeight+"px",d(t,"collapse"),d(t,"in"),f(t,"collapsing"),t.offsetWidth,t[s].height="0px",C(t,function(){t.isAnimating=!1,t.setAttribute("aria-expanded","false"),e.setAttribute("aria-expanded","false"),d(t,"collapsing"),f(t,"collapse"),t[s].height="",w.call(t,"hidden","collapse")})};this.toggle=function(t){t.preventDefault(),p(a,"in")?l.hide():l.show()},this.hide=function(){a.isAnimating||(u(a,t),f(t,"collapsed"))},this.show=function(){o&&(n=g(".collapse.in",o),i=n&&(g('[data-toggle="collapse"][data-target="#'+n.id+'"]',o)||g('[data-toggle="collapse"][href="#'+n.id+'"]',o))),(!a.isAnimating||n&&!n.isAnimating)&&(i&&n!==a&&(u(n,i),f(i,"collapsed")),c(a,t),d(t,"collapsed"))},"Collapse"in t||m(t,"click",l.toggle),a=function(){var e=t.href&&t.getAttribute("href"),n=t.getAttribute("data-target"),i=e||n&&"#"===n.charAt(0)&&n;return i&&g(i)}(),a.isAnimating=!1,o=g(e.parent)||r&&h(t,r),t.Collapse=l};o.push(["Collapse",L,'[data-toggle="collapse"]']);var y=function(t,e){for(var n=0,i=e.length;n<i;n++)new t(e[n])},x=i.initCallback=function(t){t=t||e;for(var n=0,i=o.length;n<i;n++)y(o[n][1],t.querySelectorAll(o[n][2]))};return e.body?x():m(e,"DOMContentLoaded",function(){x()}),{Collapse:L}});
// dropdown menu implementation
var el = document.getElementsByClassName('dropdown-toggle');
if (el.length) {
    el[0].addEventListener('click', function(evt){
        var parent = evt.currentTarget.parentElement;
        if (parent.className.indexOf('open') === -1) {
            parent.className += ' open';
        }
        else {
            parent.className = 'main-nav-item';
        }
        evt.preventDefault();
    });

}

// https://jsfiddle.net/cferdinandi/qgpxvhhb/18/
var login_icon = document.querySelector(".login i");
var search_icon = document.querySelector(".search i");
var search = document.getElementById("portal-searchbox");
var login = document.querySelector(".login-container");

var show = function (elem) {
    var getHeight = function () {
        elem.style.display = 'block'; 
        var height = elem.scrollHeight + 'px'; 
        elem.style.display = ''; 
        return height;
    };
    var height = getHeight(); 
    elem.classList.add('is-visible'); 
    elem.style.height = height; 
    window.setTimeout(function () {
        elem.style.height = '';
    }, 200);
};

var hide = function (elem) {
    elem.style.height = elem.scrollHeight + 'px';

    window.setTimeout(function () {
        elem.style.height = '0';
    }, 1);

    window.setTimeout(function () {
        elem.classList.remove('is-visible');
    }, 200);

};
var toggle = function (elem) {
    if (elem.classList.contains('is-visible')) {
        hide(elem);
        return;
    }
    show(elem);
};

login_icon.addEventListener('click', function(e){
    var login_classes = e.target.classList;
    var search_classes = search_icon.classList;
    if (search_classes.contains('action-selected')) {
        hide(search);
        search_icon.classList.remove('action-selected');
    }
    toggle(login);
    login_classes.toggle('action-selected');
}, false);

search_icon.addEventListener('click', function(e){
    var search_classes = e.target.classList;
    var login_classes = login_icon.classList;
    if (login_classes.contains('action-selected')) {
        hide(login);
        login_icon.classList.remove('action-selected');
    }
    toggle(search);
    search_classes.toggle('action-selected');

}, false);
