(function ($) {
    var $content_md = $('#div_id_content_md');
    var $content_ck = $('#div_id_content_ck');
    var $is_md = $('input[name=is_md]');
//    var $is_md = $('input [name=is_md]');
    var switch_editor = function (is_md) {
        if (is_md){
            //console.log('输出markdown界面');
            $content_md.show();
            $content_ck.hide();
        }
        else {
            //console.log('输出富文本界面');
            $content_md.hide();
            $content_ck.show();
        }
    }
    $is_md.on('click',function () {
        switch_editor($(this).is(':checked'));
    });
   // switch_editor($is_md.is(':checked'));
})(jQuery);