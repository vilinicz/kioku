(window.webpackJsonp=window.webpackJsonp||[]).push([[2],{172:function(t,e,r){var content=r(182);"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,r(53).default)("21ba8d80",content,!0,{sourceMap:!1})},173:function(t,e,r){var content=r(184);"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,r(53).default)("2e107364",content,!0,{sourceMap:!1})},174:function(t,e,r){"use strict";var n=r(6),o=r(175)(5),c=!0;"find"in[]&&Array(1).find((function(){c=!1})),n(n.P+n.F*c,"Array",{find:function(t){return o(this,t,arguments.length>1?arguments[1]:void 0)}}),r(72)("find")},175:function(t,e,r){var n=r(26),o=r(71),c=r(27),f=r(21),d=r(176);t.exports=function(t,e){var r=1==t,l=2==t,h=3==t,v=4==t,m=6==t,w=5==t||m,x=e||d;return function(e,d,y){for(var N,_,I=c(e),k=o(I),E=n(d,y,3),A=f(k.length),C=0,F=r?x(e,A):l?x(e,0):void 0;A>C;C++)if((w||C in k)&&(_=E(N=k[C],C,I),t))if(r)F[C]=_;else if(_)switch(t){case 3:return!0;case 5:return N;case 6:return C;case 2:F.push(N)}else if(v)return!1;return m?-1:h||v?v:F}}},176:function(t,e,r){var n=r(177);t.exports=function(t,e){return new(n(t))(e)}},177:function(t,e,r){var n=r(10),o=r(106),c=r(2)("species");t.exports=function(t){var e;return o(t)&&("function"!=typeof(e=t.constructor)||e!==Array&&!o(e.prototype)||(e=void 0),n(e)&&null===(e=e[c])&&(e=void 0)),void 0===e?Array:e}},178:function(t,e,r){"use strict";var n=r(3),o=r(15),c=r(20),f=r(107),d=r(54),l=r(9),h=r(37).f,v=r(55).f,m=r(8).f,w=r(179).trim,x=n.Number,y=x,N=x.prototype,_="Number"==c(r(70)(N)),I="trim"in String.prototype,k=function(t){var e=d(t,!1);if("string"==typeof e&&e.length>2){var r,n,o,c=(e=I?e.trim():w(e,3)).charCodeAt(0);if(43===c||45===c){if(88===(r=e.charCodeAt(2))||120===r)return NaN}else if(48===c){switch(e.charCodeAt(1)){case 66:case 98:n=2,o=49;break;case 79:case 111:n=8,o=55;break;default:return+e}for(var code,f=e.slice(2),i=0,l=f.length;i<l;i++)if((code=f.charCodeAt(i))<48||code>o)return NaN;return parseInt(f,n)}}return+e};if(!x(" 0o1")||!x("0b1")||x("+0x1")){x=function(t){var e=arguments.length<1?0:t,r=this;return r instanceof x&&(_?l((function(){N.valueOf.call(r)})):"Number"!=c(r))?f(new y(k(e)),r,x):k(e)};for(var E,A=r(7)?h(y):"MAX_VALUE,MIN_VALUE,NaN,NEGATIVE_INFINITY,POSITIVE_INFINITY,EPSILON,isFinite,isInteger,isNaN,isSafeInteger,MAX_SAFE_INTEGER,MIN_SAFE_INTEGER,parseFloat,parseInt,isInteger".split(","),C=0;A.length>C;C++)o(y,E=A[C])&&!o(x,E)&&m(x,E,v(y,E));x.prototype=N,N.constructor=x,r(11)(n,"Number",x)}},179:function(t,e,r){var n=r(6),o=r(19),c=r(9),f=r(180),d="["+f+"]",l=RegExp("^"+d+d+"*"),h=RegExp(d+d+"*$"),v=function(t,e,r){var o={},d=c((function(){return!!f[t]()||"​"!="​"[t]()})),l=o[t]=d?e(m):f[t];r&&(o[r]=l),n(n.P+n.F*d,"String",o)},m=v.trim=function(t,e){return t=String(o(t)),1&e&&(t=t.replace(l,"")),2&e&&(t=t.replace(h,"")),t};t.exports=v},180:function(t,e){t.exports="\t\n\v\f\r   ᠎             　\u2028\u2029\ufeff"},181:function(t,e,r){"use strict";var n=r(172);r.n(n).a},182:function(t,e,r){(t.exports=r(52)(!1)).push([t.i,".face-card[data-v-467829de]{padding:4vw 0 0;display:-webkit-box;display:flex;-webkit-box-orient:horizontal;-webkit-box-direction:normal;flex-flow:row nowrap;height:33.33333vh;min-height:300px;-webkit-transition:all .5s ease;transition:all .5s ease}.face-card[data-v-467829de]:not(:last-child){border-bottom:1px solid #f2f2f2}.face-card .image[data-v-467829de]{border-radius:8px;width:30vw;height:30vw;max-width:250px;max-height:250px;min-width:100px;min-height:100px;margin-right:2rem;background-repeat:no-repeat;background-size:cover;background-position:50%;flex-shrink:0}.face-card .input[data-v-467829de]{font-size:3rem;width:100%}",""])},183:function(t,e,r){"use strict";var n=r(173);r.n(n).a},184:function(t,e,r){(t.exports=r(52)(!1)).push([t.i,"#app{line-height:1.6;padding:2vw 4vw;min-height:100vh;background:-webkit-gradient(linear,left top,left bottom,from(#fff),to(#dcdcdc));background:linear-gradient(180deg,#fff,#dcdcdc)}#app,#app input{color:#2c3e50}.error{background-color:rgba(255,69,0,.6);color:#fff;font-weight:700;position:absolute;top:0;left:0;width:100%;text-align:center;padding:.5rem}.cards-enter{opacity:0;-webkit-transform:translateY(-30vh);transform:translateY(-30vh)}.cards-enter-to{opacity:1;-webkit-transform:none;transform:none}.cards-leave-to{opacity:0}.cards-leave-active{position:absolute}",""])},186:function(t,e,r){"use strict";r.r(e);r(174),r(18),r(56),r(178);var n={name:"FaceCard",props:{id:{type:Number,default:0},name:{type:String,default:""},image:{type:String,default:""},datetime:{type:Number,default:0}},data:function(){return{fname:this.name}},methods:{update:function(){return regeneratorRuntime.async((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,regeneratorRuntime.awrap(this.$axios.patch("faces/".concat(this.id),{name:this.fname}));case 2:case"end":return t.stop()}}),null,this)}}},o=(r(181),r(47)),c={components:{FaceCard:Object(o.a)(n,(function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",{staticClass:"face-card"},[r("div",{staticClass:"image",style:{backgroundImage:"url(data:image/jpeg;base64,"+t.image+")"}}),t._v(" "),r("div",{staticClass:"summary"},[r("input",{directives:[{name:"model",rawName:"v-model",value:t.fname,expression:"fname"}],staticClass:"input input-name",attrs:{placeholder:"Укажите имя",type:"text"},domProps:{value:t.fname},on:{change:t.update,input:function(e){e.target.composing||(t.fname=e.target.value)}}}),t._v(" "),r("h3",[t._v(t._s(t.datetime))])])])}),[],!1,null,"467829de",null).exports},data:function(){return{polling:null,faces:[],error:void 0}},beforeDestroy:function(){clearInterval(this.polling)},created:function(){this.pollData()},methods:{pollData:function(){var t=this;this.polling=setInterval((function(){t.get()}),1e3)},get:function(){var t,e,r;return regeneratorRuntime.async((function(n){for(;;)switch(n.prev=n.next){case 0:return t={},n.prev=1,n.next=4,regeneratorRuntime.awrap(this.$axios.get("/current_face/1"));case 4:e=n.sent,t=e.data,this.error=void 0,n.next=12;break;case 9:n.prev=9,n.t0=n.catch(1),this.error=n.t0;case 12:t.id&&(t.datetime=Date.now(),(r=this.faces.find((function(e){return e.id===t.id})))?r.datetime=Date.now():(6===this.faces.length&&this.faces.pop(),this.faces.unshift(t))),this.faces=this.faces.filter((function(t){return(Date.now()-t.datetime)/1e3<5}));case 14:case"end":return n.stop()}}),null,this,[[1,9]])}}},f=(r(183),Object(o.a)(c,(function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("div",{attrs:{id:"app"}},[t.error?r("div",{staticClass:"error"},[t._v("\n    "+t._s(t.error)+"\n  ")]):t._e(),t._v(" "),r("transition-group",{attrs:{name:"cards",tag:"div"}},t._l(t.faces,(function(e){return r("FaceCard",t._b({key:e.id},"FaceCard",e,!1))})),1)],1)}),[],!1,null,null,null));e.default=f.exports}}]);