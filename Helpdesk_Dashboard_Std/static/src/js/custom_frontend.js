colors = ['#00c0ef', '#cb6483', '#d68b5f', '#c0b66e', '#259093', '#717371'];
document.querySelectorAll('.newin').forEach((sp, i) => {
  sp.style.backgroundColor = colors[i % colors.length];
});

colors = ['2px solid #00c0ef', '2px solid #cb6483', '2px solid #d68b5f', '2px solid #c0b66e', '2px solid #259093', '2px solid #717371'];
document.querySelectorAll('.newins').forEach((sp, i) => {
  sp.style.borderBottom = colors[i % colors.length];
});


//const ticketstatus = document.querySelectorAll('.newins');
//
//ticketstatus[0].addEventListener('click', function(e) {
//    var inner_text = this.childNodes[3].childNodes[1].innerText;
//    console.log('awa'+inner_text);
//    if(inner_text == 'NEW'){
//        window.location.href = '/my/tickets?filterby=all&sortby=date&search_in=status&search=new';
//    }
//    if(inner_text == 'جديد'){
//        window.location.href = '/my/tickets?filterby=all&sortby=date&search_in=status&search=جديد';
//    }
//    
//}, false);
//
//
//ticketstatus[1].addEventListener('click', function(e) {
//    var inner_text = this.childNodes[3].childNodes[1].innerText;
//    console.log('awa'+inner_text);
//    if(inner_text == 'IN PROGRESS'){
//    window.location.href = '/my/tickets?filterby=all&sortby=date&search_in=status&search=in%20progress';
//    }
//    if(inner_text == 'قيد التنفيذ'){
//    window.location.href = '/my/tickets?filterby=all&sortby=date&search_in=status&search=قيد التنفيذ';
//    }
//}, false);
//
//
//ticketstatus[2].addEventListener('click', function(e) {
//    var inner_text = this.childNodes[3].childNodes[1].innerText;
//    if(inner_text == 'SOLVED'){
//    window.location.href = '/my/tickets?filterby=all&sortby=date&search_in=status&search=solved';
//    }
//    if(inner_text == 'تم حلّها'){
//    window.location.href = '/my/tickets?filterby=all&sortby=date&search_in=status&search=تم حلّها';
//    }
//}, false);
//
//ticketstatus[3].addEventListener('click', function(e) {
//    var inner_text = this.childNodes[3].childNodes[1].innerText;
//    if(inner_text == 'CANCELLED'){
//    window.location.href = '/my/tickets?filterby=all&sortby=date&search_in=status&search=cancelled';
//    }
//    if(inner_text == 'ملغي'){
//    window.location.href = '/my/tickets?filterby=all&sortby=date&search_in=status&search=ملغي';
//    }
//}, false);
//
//ticketstatus[4].addEventListener('click', function(e) {
//    window.location.href = '/my/tickets';
//}, false);