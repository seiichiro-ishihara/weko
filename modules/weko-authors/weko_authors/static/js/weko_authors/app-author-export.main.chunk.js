(this["webpackJsonpapp-author-export"]=this["webpackJsonpapp-author-export"]||[]).push([[0],{38:function(e,t,n){},44:function(e,t,n){"use strict";n.r(t);var r=n(0),a=n.n(r),s=n(13),c=n.n(s),o=n(26),i=n(11),l=n.n(i),d=n(17),u=n(27),m=n(28),p=n(31),x=n(30),j=(n(38),n(39),document.getElementById("errors"),document.getElementById("export_all").value),b=document.getElementById("export").value,h=document.getElementById("export_message").value,g=document.getElementById("cancel_message").value,v=document.getElementById("confirm_label").value,f=document.getElementById("run").value,O=document.getElementById("cancel").value,k=document.getElementById("download_url").value,y=document.getElementById("internal_server_error").value,E=document.getElementById("is_exporting_error").value,w=document.getElementById("cancel_export_error").value,C=JSON.parse(document.getElementById("export_authors_entrypoints").value),_=n(46),M=n(1);var N=function(e){var t=e.show,n=e.confirmMessage,r=e.onAction,a=e.onClose;return Object(M.jsxs)(_.a,{className:"opacity1",show:-1!==t,onHide:a,dialogClassName:"w-725",children:[Object(M.jsx)(_.a.Header,{closeButton:!0,children:Object(M.jsx)(_.a.Title,{className:"in-line",children:v})}),Object(M.jsx)(_.a.Body,{children:Object(M.jsx)("div",{className:"row text-center",children:n})}),Object(M.jsx)(_.a.Footer,{children:Object(M.jsx)("div",{className:"col-sm-12",children:Object(M.jsxs)("div",{className:"row text-center",children:[Object(M.jsx)("button",{variant:"primary",type:"button",className:"btn btn-default",onClick:function(){return r(1===t)},children:f}),Object(M.jsx)("button",{variant:"secondary",type:"button",className:"btn btn-default cancel",onClick:a,children:O})]})})})]})},S=n(47);var I=function(e){var t=e.type,n=void 0===t?"danger":t,r=e.msg,a=void 0===r?"":r,s=e.onClose;return""!==a?Object(M.jsx)(S.a,{variant:n,onClose:s,className:"opacity1",dismissible:!0,children:a}):""},B=function(e){Object(p.a)(n,e);var t=Object(x.a)(n);function n(){var e;return Object(u.a)(this,n),(e=t.call(this)).onAction=function(t){t?e.onExport():e.onCancel(),e.onClose()},e.onConfirm=function(t){e.setState({showConfirmModal:t?1:0,confirmMessage:t?h:g})},e.onCancel=Object(d.a)(l.a.mark((function t(){var n,r;return l.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.prev=0,t.next=3,fetch(C.cancel,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({task_id:e.state.taskId})});case 3:return n=t.sent,t.next=6,n.json();case 6:(r=t.sent).data&&"success"===r.data.status?e.setState({isExporting:!1}):e.setState({isExporting:!0,errorMsg:w}),t.next=13;break;case 10:t.prev=10,t.t0=t.catch(0),e.setState({errorMsg:y});case 13:case"end":return t.stop()}}),t,null,[[0,10]])}))),e.onExport=Object(d.a)(l.a.mark((function t(){var n,r;return l.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return e.setState({isExporting:!0}),t.next=3,e.checkExportStatus();case 3:if(t.sent){t.next=6;break}return t.abrupt("return");case 6:return t.prev=6,t.next=9,fetch(C.export,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({})});case 9:return n=t.sent,t.next=12,n.json();case 12:(r=t.sent).data&&(e.setState({taskId:r.data.task_id}),localStorage.setItem("authors_export_id",r.data.task_id),e.checkExportStatus(!0)),t.next=19;break;case 16:t.prev=16,t.t0=t.catch(6),e.setState({isExporting:!1,errorMsg:y});case 19:case"end":return t.stop()}}),t,null,[[6,16]])}))),e.checkExportStatus=Object(d.a)(l.a.mark((function t(){var n,r=arguments;return l.a.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return n=r.length>0&&void 0!==r[0]&&r[0],e.setState({isChecking:!0,errorMsg:""}),t.next=4,new Promise((function(t){var r=setInterval(Object(d.a)(l.a.mark((function a(){var s,c,i,d,u;return l.a.wrap((function(a){for(;;)switch(a.prev=a.next){case 0:return s={},a.prev=1,c=e.state.taskId,a.next=5,fetch(C.check_status,{method:"GET"});case 5:return i=a.sent,a.next=8,i.json();case 8:(d=a.sent).data?(u=d.data).task_id&&c===u.task_id?(s.isExporting=!0,n=!0):u.task_id?s.errorMsg=E:(n&&(n=!1,s.isExporting=!1),s.downloadLink=u.download_link):s.errorMsg=y,a.next=15;break;case 12:a.prev=12,a.t0=a.catch(1),s.errorMsg=y;case 15:s.errorMsg&&(s.isExporting=!1),!n||s.errorMsg?(e.setState(Object(o.a)({isChecking:!1},s)),t(""===e.state.errorMsg&&!s.isExporting),clearInterval(r)):e.setState(Object(o.a)({},s));case 17:case"end":return a.stop()}}),a,null,[[1,12]])}))),1e3)}));case 4:return t.abrupt("return",t.sent);case 5:case"end":return t.stop()}}),t)}))),e.onClose=function(){e.setState({showConfirmModal:-1})},e.state={showConfirmModal:-1,isDisableExport:!1,isDisableCancel:!0,confirmMessage:"",isChecking:!1,isExporting:!1,errorMsg:"",taskId:localStorage.getItem("authors_export_id"),downloadLink:""},e}return Object(m.a)(n,[{key:"componentDidMount",value:function(){this.checkExportStatus()}},{key:"render",value:function(){var e=this,t=this.state,n=t.errorMsg,r=t.downloadLink,a=t.isExporting,s=t.isChecking,c=t.showConfirmModal,o=t.confirmMessage;return Object(M.jsxs)(M.Fragment,{children:[Object(M.jsxs)("div",{className:"col-sm-12",children:[Object(M.jsx)(I,{type:"danger",msg:n,onClose:function(){return e.setState({errorMsg:""})}}),Object(M.jsx)("div",{className:"row",children:Object(M.jsx)("div",{className:"col-sm-12",children:Object(M.jsx)("label",{children:j})})}),Object(M.jsx)("div",{className:"row",children:Object(M.jsxs)("div",{className:"col-sm-12 text-center",children:[Object(M.jsxs)("button",{disabled:a||s,type:"button",className:"btn btn-primary margin",onClick:function(){return e.onConfirm(!0)},children:[a||s?Object(M.jsx)("div",{className:"loading"}):Object(M.jsx)(M.Fragment,{}),b]}),Object(M.jsx)("button",{disabled:!a,type:"button",className:"btn btn-primary margin cancel",onClick:function(){return e.onConfirm(!1)},children:O})]})}),Object(M.jsx)("div",{className:"row",children:Object(M.jsx)("div",{className:"col-sm-12",children:Object(M.jsx)("label",{children:k})})}),Object(M.jsx)("div",{className:"row",children:Object(M.jsx)("div",{className:"col-sm-12",children:Object(M.jsx)("a",{href:r,children:r})})})]}),Object(M.jsx)(N,{show:c,confirmMessage:o,onAction:this.onAction,onClose:this.onClose})]})}}]),n}(a.a.Component);c.a.render(Object(M.jsx)(a.a.StrictMode,{children:Object(M.jsx)(B,{})}),document.getElementById("app-author-export"))}},[[44,1,2]]]);
//# sourceMappingURL=main.c0ad9176.chunk.js.map