(window.webpackJsonp=window.webpackJsonp||[]).push([[2],{172:function(e,t,r){var content=r(182);"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,r(53).default)("18ebf17d",content,!0,{sourceMap:!1})},173:function(e,t,r){var content=r(184);"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,r(53).default)("0ace817b",content,!0,{sourceMap:!1})},174:function(e,t,r){"use strict";var n=r(6),o=r(175)(5),c=!0;"find"in[]&&Array(1).find((function(){c=!1})),n(n.P+n.F*c,"Array",{find:function(e){return o(this,e,arguments.length>1?arguments[1]:void 0)}}),r(72)("find")},175:function(e,t,r){var n=r(26),o=r(71),c=r(27),d=r(21),l=r(176);e.exports=function(e,t){var r=1==e,f=2==e,m=3==e,h=4==e,v=6==e,x=5==e||v,w=t||l;return function(t,l,y){for(var N,k,I=c(t),_=o(I),C=n(l,y,3),A=d(_.length),E=0,F=r?w(t,A):f?w(t,0):void 0;A>E;E++)if((x||E in _)&&(k=C(N=_[E],E,I),e))if(r)F[E]=k;else if(k)switch(e){case 3:return!0;case 5:return N;case 6:return E;case 2:F.push(N)}else if(h)return!1;return v?-1:m||h?h:F}}},176:function(e,t,r){var n=r(177);e.exports=function(e,t){return new(n(e))(t)}},177:function(e,t,r){var n=r(10),o=r(106),c=r(2)("species");e.exports=function(e){var t;return o(e)&&("function"!=typeof(t=e.constructor)||t!==Array&&!o(t.prototype)||(t=void 0),n(t)&&null===(t=t[c])&&(t=void 0)),void 0===t?Array:t}},178:function(e,t,r){"use strict";var n=r(3),o=r(15),c=r(20),d=r(107),l=r(54),f=r(9),m=r(37).f,h=r(55).f,v=r(8).f,x=r(179).trim,w=n.Number,y=w,N=w.prototype,k="Number"==c(r(70)(N)),I="trim"in String.prototype,_=function(e){var t=l(e,!1);if("string"==typeof t&&t.length>2){var r,n,o,c=(t=I?t.trim():x(t,3)).charCodeAt(0);if(43===c||45===c){if(88===(r=t.charCodeAt(2))||120===r)return NaN}else if(48===c){switch(t.charCodeAt(1)){case 66:case 98:n=2,o=49;break;case 79:case 111:n=8,o=55;break;default:return+t}for(var code,d=t.slice(2),i=0,f=d.length;i<f;i++)if((code=d.charCodeAt(i))<48||code>o)return NaN;return parseInt(d,n)}}return+t};if(!w(" 0o1")||!w("0b1")||w("+0x1")){w=function(e){var t=arguments.length<1?0:e,r=this;return r instanceof w&&(k?f((function(){N.valueOf.call(r)})):"Number"!=c(r))?d(new y(_(t)),r,w):_(t)};for(var C,A=r(7)?m(y):"MAX_VALUE,MIN_VALUE,NaN,NEGATIVE_INFINITY,POSITIVE_INFINITY,EPSILON,isFinite,isInteger,isNaN,isSafeInteger,MAX_SAFE_INTEGER,MIN_SAFE_INTEGER,parseFloat,parseInt,isInteger".split(","),E=0;A.length>E;E++)o(y,C=A[E])&&!o(w,C)&&v(w,C,h(y,C));w.prototype=N,N.constructor=w,r(11)(n,"Number",w)}},179:function(e,t,r){var n=r(6),o=r(19),c=r(9),d=r(180),l="["+d+"]",f=RegExp("^"+l+l+"*"),m=RegExp(l+l+"*$"),h=function(e,t,r){var o={},l=c((function(){return!!d[e]()||"​"!="​"[e]()})),f=o[e]=l?t(v):d[e];r&&(o[r]=f),n(n.P+n.F*l,"String",o)},v=h.trim=function(e,t){return e=String(o(e)),1&t&&(e=e.replace(f,"")),2&t&&(e=e.replace(m,"")),e};e.exports=h},180:function(e,t){e.exports="\t\n\v\f\r   ᠎             　\u2028\u2029\ufeff"},181:function(e,t,r){"use strict";var n=r(172);r.n(n).a},182:function(e,t,r){(e.exports=r(52)(!1)).push([e.i,".face-card[data-v-6da81ae1]{padding:1rem;display:-webkit-box;display:flex;-webkit-box-orient:vertical;-webkit-box-direction:normal;flex-flow:column;-webkit-box-pack:center;justify-content:center;-webkit-transition:all .4s ease,background-color 1.5s ease-in-out;transition:all .4s ease,background-color 1.5s ease-in-out}.face-card[data-v-6da81ae1]:not(:last-child){border-bottom:1px solid #ebeef5}.face-card .wrapper[data-v-6da81ae1]{display:-webkit-box;display:flex;-webkit-box-orient:horizontal;-webkit-box-direction:normal;flex-flow:row nowrap}.face-card .image[data-v-6da81ae1]{position:relative;border-radius:16px;width:28vw;height:28vw;max-width:230px;max-height:230px;min-width:100px;min-height:100px;margin-right:1rem;background-color:#f2f6fc;background-repeat:no-repeat;background-size:cover;background-position:50%;flex-shrink:0;box-shadow:inset 0 0 10px rgba(0,0,0,.2)}.face-card .image .status[data-v-6da81ae1]{position:absolute;top:-8px;right:-8px;width:26px;height:26px;box-shadow:0 0 0 4px #fff;border-radius:13px;background-color:#dcdfe6}.face-card .image .status.on[data-v-6da81ae1]{background-color:#67c23a}@media (min-width:768px){.face-card .image[data-v-6da81ae1]{margin-right:2rem}}.face-card .wrap[data-v-6da81ae1]{display:-webkit-box;display:flex;-webkit-box-orient:horizontal;-webkit-box-direction:normal;flex-flow:row nowrap}.face-card .wrap .input-name[data-v-6da81ae1]{margin-right:1rem;flex-basis:75%}.face-card .wrap .input-room[data-v-6da81ae1]{flex-basis:25%;text-align:right;font-weight:500}.face-card .input[data-v-6da81ae1]{font-size:1.4rem;width:100%;color:#2c3e50;background-color:#f2f6fc;margin-bottom:1rem;padding:.25rem .5rem;border-radius:8px}@media (min-width:768px){.face-card .input[data-v-6da81ae1]{font-size:2.2rem;padding:.25rem 1rem}}.face-card .input-note[data-v-6da81ae1]{font-size:1.2rem;resize:none;margin-bottom:0;display:block}@media (min-width:768px){.face-card .input-note[data-v-6da81ae1]{font-size:1.75rem}}@media (min-width:768px){.face-card[data-v-6da81ae1]{padding:2rem}}",""])},183:function(e,t,r){"use strict";var n=r(173);r.n(n).a},184:function(e,t,r){(e.exports=r(52)(!1)).push([e.i,"#app{line-height:1.6;min-height:100vh;font-family:Avenir Next,sans-serif}#app,#app input{color:#303133}.error{background-color:rgba(245,108,108,.8);color:#fff;font-weight:700;position:absolute;top:0;left:0;width:100%;text-align:center;padding:.75rem;z-index:99}.cards-enter{opacity:0;-webkit-transform:translateY(-30vh);transform:translateY(-30vh);background-color:#fefbec}.cards-enter-to{opacity:1;-webkit-transform:none;transform:none;background-color:#fff}.cards-leave-to{opacity:0}.cards-leave-active{position:absolute}",""])},186:function(e,t,r){"use strict";r.r(t);r(174),r(18),r(56),r(178);var n={name:"FaceCard",props:{id:{type:Number,default:0},name:{type:String,default:""},room:{type:Number,default:void 0},note:{type:String,default:""},image:{type:String,default:""},datetime:{type:Number,default:0}},data:function(){return{editableName:this.name,editableRoom:this.room,editableNote:this.note,refreshing:null,online:!0}},beforeDestroy:function(){clearInterval(this.refreshing)},created:function(){this.refresh()},methods:{update:function(){var e;return regeneratorRuntime.async((function(t){for(;;)switch(t.prev=t.next){case 0:return e={name:this.editableName,room:this.editableRoom,note:this.editableNote},t.next=3,regeneratorRuntime.awrap(this.$axios.patch("faces/".concat(this.id),e));case 3:case"end":return t.stop()}}),null,this)},refresh:function(){var e=this;this.refreshing=setInterval((function(){e.online=(Date.now()-e.datetime)/1e3<3,(Date.now()-e.datetime)/1e3>180&&e.$emit("destroy",e.id)}),1e3)}}},o=(r(181),r(47)),c={components:{FaceCard:Object(o.a)(n,(function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"face-card"},[r("div",{staticClass:"wrapper"},[r("div",{staticClass:"image",style:{backgroundImage:"url(data:image/jpeg;base64,"+e.image+")"}},[r("div",{staticClass:"status",class:{on:e.online}})]),e._v(" "),r("form",{staticClass:"summary",attrs:{action:"#"}},[r("div",{staticClass:"wrap"},[r("input",{directives:[{name:"model",rawName:"v-model",value:e.editableName,expression:"editableName"}],staticClass:"input input-name",attrs:{placeholder:"Имя",type:"text"},domProps:{value:e.editableName},on:{change:e.update,input:function(t){t.target.composing||(e.editableName=t.target.value)}}}),e._v(" "),r("input",{directives:[{name:"model",rawName:"v-model",value:e.editableRoom,expression:"editableRoom"}],staticClass:"input input-room",attrs:{placeholder:"#",type:"number",min:"0",inputmode:"numeric",pattern:"[0-9]*"},domProps:{value:e.editableRoom},on:{change:e.update,input:function(t){t.target.composing||(e.editableRoom=t.target.value)}}})]),e._v(" "),r("textarea",{directives:[{name:"model",rawName:"v-model",value:e.editableNote,expression:"editableNote"}],staticClass:"input input-note",attrs:{rows:"4",placeholder:"Дополнительно",type:"text"},domProps:{value:e.editableNote},on:{change:e.update,input:function(t){t.target.composing||(e.editableNote=t.target.value)}}})])])])}),[],!1,null,"6da81ae1",null).exports},data:function(){return{polling:null,sorting:null,faces:[],error:void 0}},beforeDestroy:function(){clearInterval(this.polling),clearInterval(this.sorting)},created:function(){this.pollData(),this.sortFaces()},methods:{removeOldFace:function(e){this.faces=this.faces.filter((function(t){return t.id!==e}))},sortFaces:function(){var e=this;this.polling=setInterval((function(){e.faces=e.faces.sort((function(a,b){return b.datetime-a.datetime}))}),2e3)},pollData:function(){var e=this;this.polling=setInterval((function(){e.get()}),1e3)},get:function(){var e,t,r;return regeneratorRuntime.async((function(n){for(;;)switch(n.prev=n.next){case 0:return e={},n.prev=1,n.next=4,regeneratorRuntime.awrap(this.$axios.get("/current_face/1"));case 4:t=n.sent,e=t.data,this.error=void 0,n.next=12;break;case 9:n.prev=9,n.t0=n.catch(1),this.error=n.t0;case 12:e.id&&(e.datetime=Date.now(),(r=this.faces.find((function(t){return t.id===e.id})))?((Date.now()-r.datetime)/1e3>3&&(r.image=e.image),r.datetime=Date.now()):(8===this.faces.length&&this.faces.pop(),this.faces.unshift(e)));case 13:case"end":return n.stop()}}),null,this,[[1,9]])}}},d=(r(183),Object(o.a)(c,(function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{attrs:{id:"app"}},[e.error?r("div",{staticClass:"error"},[e._v("\n    "+e._s(e.error)+"\n  ")]):e._e(),e._v(" "),r("transition-group",{attrs:{name:"cards",tag:"div"}},e._l(e.faces,(function(t){return r("FaceCard",e._b({key:t.id,on:{destroy:e.removeOldFace}},"FaceCard",t,!1))})),1)],1)}),[],!1,null,null,null));t.default=d.exports}}]);