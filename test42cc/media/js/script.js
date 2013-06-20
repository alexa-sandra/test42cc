$(function(){
     $('#form_id').submit(function(){
           $(this).ajaxSubmit({
                 beforeSend: function(){
                      $('#progress').show();
                      $('input:submit').attr("disabled","disabled");
                                             },
                 success : function() {
                      $('#progress').hide();
                      $('input:submit').removeAttr("disabled");
                                          }
                                       });
                   return false;
                                              });
                   });
