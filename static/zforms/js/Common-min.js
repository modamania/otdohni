/**
 * Common functions
 * -----------------------------------------------
 * @author        Filatov Dmitry <alpha@zforms.ru>
 * @version       0.51, 06.07.2009
 */

var Common={Browser:{bIE:!!(window.attachEvent&&!window.opera),bOpera:!!window.opera,bSafari:/webkit/i.test(navigator.userAgent),bMozilla:/mozilla/i.test(navigator.userAgent)&&!/(compatible|webkit)/i.test(navigator.userAgent),isIE:function(){return this.bIE},isOpera:function(){return this.bOpera},isSafari:function(){return this.bSafari},isMozilla:function(){return this.bMozilla}},Class:{match:function(b,a){return b.className!=""&&(" "+b.className+" ").indexOf(" "+a+" ")>-1},add:function(b,a){if(!this.match(b,a)){b.className+=" "+a}},replace:function(b,c,d,a){if(this.match(b,c)){b.className=(b.className.replace(new RegExp("(^|\\s+)("+c+"|"+d+")($|\\s+)","g"),"$1")+" "+d).replace(/^\s+/,"")}else{if(a&&this.match(b,d)){b.className=(b.className.replace(new RegExp("(^|\\s+)("+d+"|"+c+")($|\\s+)","g"),"$1")+" "+c).replace(/^\s+/,"")}else{this.add(b,d)}}},remove:function(b,a){b.className=b.className.replace(new RegExp("(.*)(^|\\s+)("+a+")($|\\s+)(.*)"),"$1$4$5").replace(/(^)\s/,"$1")}},Event:{aObservers:[],TYPE_DOM_CONTENT_LOADED:"DOMContentLoaded",add:function(c,a,d){var b=0;if(Common.Utils.isArray(c)||(c.item&&c.length&&!c.tagName)){while(c[b]){this.add(c[b++],a,d)}return}if(Common.Utils.isArray(a)){while(a[b]){this.add(c,a[b++],d)}return}if(a==this.TYPE_DOM_CONTENT_LOADED){return this.addDomContentLoaded(c,d)}if(c.addEventListener){c.addEventListener(a,d,false)}else{if(c.attachEvent){this.attachObserver(c,a,d);c.attachEvent("on"+a,d)}}},remove:function(c,a,d){var b=0;if(Common.Utils.isArray(c)||(c.item&&c.length&&!c.tagName)){while(c[b]){this.remove(c[b++],a,d)}return}if(Common.Utils.isArray(a)){while(a[b]){this.remove(c,a[b++],d)}return}if(a==this.TYPE_DOM_CONTENT_LOADED){return this.removeDomContentLoaded(c,d)}if(c.removeEventListener){c.removeEventListener(a,d,false)}else{if(c.detachEvent){c.detachEvent("on"+a,d)}}},addDomContentLoaded:function(a,b){if(document.addEventListener&&!/webkit/i.test(navigator.userAgent)){document.addEventListener(this.TYPE_DOM_CONTENT_LOADED,b,false)}else{if(this.aObservers.indexOfByFunction(this.TYPE_DOM_CONTENT_LOADED,function(c,d){return c[1]==d})>-1){this.attachObserver(a,this.TYPE_DOM_CONTENT_LOADED,b);return}this.attachObserver(a,this.TYPE_DOM_CONTENT_LOADED,b);if(document.addEventListener){setTimeout(function(){if(document.readyState=="loaded"||document.readyState=="complete"){Common.Event.fireDomContentLoaded()}else{setTimeout(arguments.callee,10)}},10)}else{(function(){var c=document.createElement("document:ready");try{c.doScroll("left");c=null;Common.Event.fireDomContentLoaded()}catch(d){setTimeout(arguments.callee,10)}})()}}},removeDomContentLoaded:function(c,d){if(document.addEventListener&&!/webkit/i.test(navigator.userAgent)){return document.removeEventListener(this.TYPE_DOM_CONTENT_LOADED,d,false)}var a=this.aObservers.filtrate(d,function(e,f){return e[1]==Common.Event.TYPE_DOM_CONTENT_LOADED&&e[2]==f});var b=0;while(a[b]){this.aObservers.remove(a[b++])}},fireDomContentLoaded:function(){var a=this.aObservers.filtrate(this.TYPE_DOM_CONTENT_LOADED,function(c,d){return c[1]==d});var b=0;while(a[b]){a[b++][2]()}},attachObserver:function(a,c,b){this.aObservers.push([a,c,b]);if(this.aObservers.length==1){this.add(window,"unload",function(){Common.Event.detachObservers()})}},detachObservers:function(){var a=0;while(this.aObservers[a]){this.remove(this.aObservers[a][0],this.aObservers[a][1],this.aObservers[a][2]);this.aObservers[a++][0]=null}this.aObservers.length=0},cancel:function(a){var a=a?a:window.event;a.cancelBubble=true;a.returnValue=false;if(a.cancelable){a.preventDefault();a.stopPropagation()}return false},normalize:function(a){var a=a?a:window.event;if(a&&a.srcElement&&!window.opera){a.target=a.srcElement}if(a){a.iKeyCode=a.keyCode?a.keyCode:(a.which?a.which:null);if(a.wheelDelta){a.iMouseWheelDelta=a.wheelDelta/120;if(window.opera){a.iMouseWheelDelta*=-1}}else{if(a.detail){a.iMouseWheelDelta=-a.detail/3}}}return a},getAbsoluteCoords:function(b){var b=b?b:window.event,c={iLeft:0,iTop:0};if(b.pageX||b.pageY){c.iLeft=b.pageX;c.iTop=b.pageY}else{if(b.clientX||b.clientY){c.iLeft=b.clientX+document.body.scrollLeft-document.body.clientLeft;c.iTop=b.clientY+document.body.scrollTop-document.body.clientTop;var a=document.documentElement;if(a){c.iLeft+=a.scrollLeft-a.clientLeft;c.iTop+=a.scrollTop-a.clientTop}}}return c}},Dom:{NODE_TYPE_ELEMENT:1,NODE_TYPE_TEXT:3,getUniqueId:function(a){return Common.Utils.getUniqueId(a)},getAbsoluteCoords:function(a){var b={iTop:0,iLeft:0};while(a){b.iTop+=a.offsetTop;b.iLeft+=a.offsetLeft;a=a.offsetParent}return b},getAttribute:function(b,c){if(b.attributes){var a=0;while(b.attributes[a]){if(b.attributes[a++].nodeName==c){return b.attributes[a-1].nodeValue}}}return b.getAttribute(c)},createElement:function(d,c,e){var b;if(Common.Browser.isIE()){var a="<"+d;if(c){c.foreach(function(g,f){if(typeof(f)!="undefined"){a+=" "+g+'="'+f+'"'}})}b=document.createElement(a+" />")}else{b=document.createElement(d);if(c){c.foreach(function(g,f){if(typeof(f)!="undefined"){b.setAttribute(g,f)}})}}if(e){b.innerHTML=e}return b},getElementsByClassName:function(c,a,b,d){if(document.querySelectorAll){if(Common.Browser.isIE()){this.getElementsByClassName=function(j,f,g,m){var e=j.querySelectorAll((m?">":"")+(g?g:"")+"."+f),l=[],h=0,k;while(k=e[h++]){l.push(k)}return l}}else{this.getElementsByClassName=function(g,e,f,h){return[].slice.call(g.querySelectorAll((h?">":"")+(f?f:"")+"."+e),0)}}}else{if(document.evaluate){this.getElementsByClassName=function(h,e,f,l){oQueryResult=document.evaluate("./"+(l?"":"/")+(f||"*")+"[contains(concat(' ', @class, ' '), ' "+e+" ')]",h,null,XPathResult.ORDERED_NODE_SNAPSHOT_TYPE,null);var g=0,k=[],j;while(j=oQueryResult.snapshotItem(g++)){k.push(j)}return k}}else{this.getElementsByClassName=function(h,e,f,m){var l=[],f=f||"*",g=0,j;if(m){while(j=h.childNodes[g++]){if(j.nodeType==this.NODE_TYPE_ELEMENT&&(f=="*"||j.tagName.toLowerCase()==f)&&Common.Class.match(j,e)){l.push(j)}}return l}var k=f=="*"&&h.all?h.all:h.getElementsByTagName(f);while(j=k[g++]){if(Common.Class.match(j,e)){l.push(j)}}return l}}}return this.getElementsByClassName(c,a,b,d)},setStyle:function(b,a){if(typeof(b.style.cssText)!="undefined"){b.style.cssText=a}else{b.setAttribute("style",a)}},setOpacity:function(b,a){if(b.runtimeStyle){b.style.zoom=1;b.style.filter=b.style.filter.replace(/alpha\([^)]*\)/,"")+"alpha(opacity="+a*100+")"}else{if(a==1){b.style.opacity=""}else{b.style.opacity=a}}}},Cookie:{set:function(c,d,b,a){document.cookie=c+"="+(window.encodeURI?encodeURI(d):escape(d))+((b==null)?"":("; expires="+b.toGMTString()))+((a==null)?"":("; path="+a))},get:function(d){var c=d+"=";if(document.cookie.length>0){var b=document.cookie.indexOf(c);if(b!=-1){b+=c.length;var a=document.cookie.indexOf(";",b);if(a==-1){a=document.cookie.length}return window.decodeURI?decodeURI(document.cookie.substring(b,a)):unescape(document.cookie.substring(b,a))}}return""}},Object:{extend:function(d,a,c){if(!a){return d}var d=d||{};for(var b in a){if((c||typeof(d[b])=="undefined")&&typeof(a[b])!="undefined"){d[b]=a[b]}}return d}},Observable:{aObservers:[],attach:function(d,f,c){var e=0;if(Common.Utils.isArray(d)){while(d[e]){this.attach(d[e++],f,c)}return}if(Common.Utils.isArray(f)){while(f[e]){this.attach(d,f[e++],c)}return}if(Common.Utils.isArray(c)){while(c[e]){this.attach(d,f,c[e++])}return}if(!this.aObservers[d]){this.aObservers[d]=[]}var b=this.aObservers[d],a=Common.Utils.getUniqueId(c);if(!b[a]){b[a]=[]}b[a].push(f)},detach:function(d,f,c){var e=0;if(Common.Utils.isArray(d)){while(d[e]){this.detach(d[e++],f,c)}return}if(Common.Utils.isArray(f)){while(f[e]){this.detach(d,f[e++],c)}return}if(Common.Utils.isArray(c)){while(c[e]){this.detach(d,f,c[e++])}return}var b=this.aObservers[d];if(!b){return}var a=Common.Utils.getUniqueId(c);if(b[a]){b[a].remove(f)}},notify:function(f,h,e){var c=this.aObservers[f];if(!c){return}var b=Common.Utils.getUniqueId(h);if(!c[b]){return}var d=0,a=c[b],g;while(g=a[d++]){g(f,h,e)}}},Utils:{oPopupDefaults:{iWidth:540,iHeight:600,sToolbar:"no",sMenubar:"no",sResizeable:"yes",sScrollbars:"yes",sStatus:"yes"},popup:function(d,e,c){c=Common.Object.extend(Common.Utils.oPopupDefaults,c,true);var a=screen.availWidth/2-c.iWidth/2;var b=screen.availHeight/2-c.iHeight/2;oNewWindow=window.open(d,"","left="+a+", top = "+b+", width="+c.iWidth+", height="+c.iHeight+", menubar="+c.sMenubar+", toolbar="+c.sToolbar+", resizable="+c.sResizeable+", scrollbars="+c.sScrollbars+", status="+c.sStatus);if(d.match(/\.(gif|jpe?g|png)$/i)){oNewWindow.document.open();oNewWindow.document.write("<html><head>"+(e!=""?"<title>"+e+"</title>":"")+'</head><body style="background: #FFF; margin: 0; padding: 0;"><table cellpadding="0" cellspacing="0" border="0" width="100%" height="100%"><tr><td align="center"><img src="'+d+'" /></td></tr></table></body></html>');oNewWindow.document.close()}oNewWindow.focus();return false},aNavigationLinks:[{sRel:"next",iKeyCode:39,sHref:""},{sRel:"prev",iKeyCode:37,sHref:""},{sRel:"up",iKeyCode:38,sHref:""},{sRel:"down",iKeyCode:40,sHref:""},{sRel:"start",iKeyCode:36,sHref:""}],keyNavigationInit:function(){var d=document.getElementsByTagName("link"),c,b=0,a=0;while(c=d[b++]){a=0;while(this.aNavigationLinks[a]){if(this.aNavigationLinks[a++].sRel===c.rel){this.aNavigationLinks[a-1].sHref=c.href;break}}}Common.Event.add(document,"keydown",function(g){var g=Common.Event.normalize(g);if(!g.ctrlKey){return true}var f=g.target.tagName.toLowerCase();if(f=="input"||f=="textarea"){return}var e=Common.Utils.aNavigationLinks,h=0;while(e[h++]){if(e[h-1].iKeyCode==g.iKeyCode&&e[h-1].sHref!=""){document.location=e[h-1].sHref}}})},getUniqueId:function(a){if(a.uniqueID){return a.uniqueID}if(!arguments.callee.counter){arguments.callee.counter=0}a.uniqueID="__uid-"+arguments.callee.counter++;return a.uniqueID},isArray:function(a){return Object.prototype.toString.call(a)==="[object Array]"}}};Common.Object.extend(Object.prototype,{hasOwnProperty:function(a){return !("undefined"==typeof this[a]||this.constructor&&this.constructor.prototype[a]&&this[a]===this.constructor.prototype[a])},foreach:function(b){for(var a in this){if(this.hasOwnProperty(a)){b(a,this[a])}}}});Common.Object.extend(Function.prototype,{inheritTo:function(c,e){var b=this,f=function(){if(this.__constructor){this.__constructor.apply(this,arguments)}},d=function(){};Common.Object.extend(f,b);d.prototype=this.prototype;f.prototype=new d();f.prototype.constructor=f;f.prototype.__self=f;if(c){for(var a in c){if(typeof(f.prototype[a])=="function"){(function(g){f.prototype[g]=function(){var i=this.__base;this.__base=b.prototype[g];var h=c[g].apply(this,arguments);this.__base=i;return h}})(a)}else{f.prototype[a]=c[a]}}}if(e){Common.Object.extend(f,e,true)}return f},delay:function(c,a,d){var b=this;setTimeout(function(){b.call(a||window,d)},c)}});Common.Object.extend(Array.prototype,{isEmpty:function(){return this.length==0},remove:function(b){for(var a=0;a<this.length;a++){if(this[a]==b){this.splice(a,1);break}}},indexOf:function(b){for(var a=0;a<this.length;a++){if(this[a]==b){return a}}return -1},indexOfByFunction:function(b,c){if(!c){return this.indexOf(b)}for(var a=0;a<this.length;a++){if(c(this[a],b)){return a}}return -1},contains:function(a,b){return this.indexOfByFunction(a,b)>-1},filtrate:function(b,d){var c=[];for(var a=0;a<this.length;a++){if(d(this[a],b)){c.push(this[a])}}return c},intersect:function(b){var c=[];for(var a=0;a<b.length;a++){if(this.contains(b[a])){c.push(b[a])}}return c},union:function(b){var c=[].concat(this);for(var a=0;a<b.length;a++){if(!this.contains(b[a])){c.push(b[a])}}return c},subtract:function(b){var c=[].concat(this);for(var a=0;a<b.length;a++){if(this.contains(b[a])){c.remove(b[a])}}return c},unique:function(){var c=[],a=-1,b;while((b=this[++a])!=null){if(!this[a].__marked){this[a].__marked=true;c.push(b)}}while(b=this[--a]){this[a].__marked=undefined}return c}});Common.Object.extend(String.prototype,{stripTags:function(){return this.replace(/<\/?[^>]+>/gi,"")},formatNumber:function(a,e){var a=a||" ",e=e||",",d=this.indexOf("."),c=d>-1?this.substring(d+1):"",f=d>-1?this.substring(0,d):this;if(f.length<5){return f+(d>-1?e+c:"")}var b="";while(f.length>3){b=f.substring(f.length-3)+(b.length>0?a:"")+b;f=f.substring(0,f.length-3)}b=f+a+b+(d>-1?e+c:"");return b}});Common.Object.extend(Number.prototype,{toFixed:function(b){var a=this.toString().split(".",2);if(!a[1]){return this}return a[0]+"."+Math.round(a[1]/Math.pow(10,a[1].length-b))},formatNumber:function(a,b){return this.toString().formatNumber(a,b)}});function Abstract(){throw ("abstract class")}Common.Utils.StringBuffer=Abstract.inheritTo({__constructor:function(a){this.aBuffer=[];if(a){this.append(a)}},append:function(a){this.aBuffer.push(a);return this},get:function(){return this.aBuffer.join("")},clear:function(){this.aBuffer=[];return this}});document.documentElement.id="with-js";Common.Event.add(window,"error",function(){var a=document.getElementsByTagName("body")[0];if(!a){return}Common.Class.add(a,"with-js-error")});Common.Event.add(document,Common.Event.TYPE_DOM_CONTENT_LOADED,function(){Common.Utils.keyNavigationInit()});