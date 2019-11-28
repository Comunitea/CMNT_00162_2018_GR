$(document).ready(function(){
    $(".s_website_form").validate({
      rules: {
        email_from: {
          required: true,
          email: true
        },
        phone: {
          required: true,
        }
      },
      messages: {
        email_from: {
            required: 'Este campo es obligatorio',
            email: 'Por favor, introduce una dirección de correo electrónico válida'
        },
        phone: {
            required: 'Este campo es obligatorio'
        }
      }
    });

    /* add menu cart item active class*/
//    $('.nav .fa-shopping-cart').closest('li').addClass('always_hover');

    /* select rent dates section */
    function calcDates(){

        var start_date = $('input[name="start-date"]').val();
        var rental_selected = $('select[name="week-duration"] option').filter(':selected').val().split('-');
        var weeks = parseInt(rental_selected[0]);
        var quantity = parseInt(weeks * 7);
        var price = parseFloat(rental_selected[1]);
        var price_total = parseFloat(price * weeks);

        /* "start date" and "end date" calculation */
        if(start_date && weeks){
            var start_date_new = new Date(start_date);
            var start_math = Date.parse(start_date_new);
            var end_math = Math.abs(start_math + (864e5 * ((quantity) - 1)));
            var end_date = new Date(end_math);
            var end_day   = ('0' + (end_date.getDate())).slice(-2);
            var end_month = ('0' + (end_date.getMonth() + 1)).slice(-2);
            var end_year  = end_date.getFullYear();
            var parse_end_date = end_year+'-'+end_month+'-'+end_day;
            $('input[name="end-date"]').val(parse_end_date)
            $('input[name="add_qty"]').val(parseInt(weeks));

            if(price_total){
                /* sale_rental fields */
                var number_of_days = Math.abs(quantity);
                $('input[name="number_of_days"]').val(number_of_days)
                $('input[name="start_date"]').val(start_date)
                $('input[name="end_date"]').val(parse_end_date)

                /* show "add to cart" button and price */
                $('span.dates-total-price').html(price_total);
                $('.form-control-dates-select').hide();
                $('.form-control-dates-total').show();
                $('a#add_to_cart').show();
            }
        }
    }
    $('input[name="start-date"]').on('change', function(){
//        No necessary by t-att-min date picker
//        $('#date_info').hide();
//        var current_date = new Date();
//        current_date.setHours(0);
//        current_date.setMinutes(0);
//        current_date.setMilliseconds(0);
//        var start_date = new Date($('input[name="start-date"]').val());
//        No necessary by hide-show form-control-dates-select and form-control-dates-quantity
//        if (start_date.getTime() < current_date.getTime()){
//            $('a#add_to_cart').addClass('hidden');
//            $('#date_error').removeClass('hidden');
//        } else {
//            $('a#add_to_cart').removeClass('hidden');
//            $('#date_error').addClass('hidden');
//        }
        calcDates();
    });
    $('select[name="week-duration"]').on('change', function(){
        calcDates();
    });
    $('.oe_price span.oe_currency_value').on('change', function(){
        calcDates();
    })
    $('.form-control.js_variant_change').on('change', function(){
        setTimeout(function(){
            $('.oe_price span.oe_currency_value').trigger('change');
        }, 50);
    });
    //
});
