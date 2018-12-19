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
    $('.nav .fa-shopping-cart').closest('li').addClass('always_hover');

    /* select rent dates section */
    function calcDates(){

        var start_date = $('input[name="start-date"]').val()
            weeks = $('select[name="week-duration"] option').filter(':selected').val()

        /* "start date" and "end date" calculation */
        if(start_date && weeks){

            var start_date_new = new Date(start_date)
                start_math = Date.parse(start_date_new)
                end_math = Math.abs(start_math + (864e5 * ((7 * weeks) - 1)))
                end_date = new Date(end_math)
                end_day   = ('0' + (end_date.getDate() + 1)).slice(-2)
                end_month = ('0' + (end_date.getMonth() + 1)).slice(-2)
                end_year  = end_date.getFullYear()
                parse_end_date = end_year+'-'+end_month+'-'+end_day

            $('input[name="end-date"]').val(parse_end_date)

            /* price and weeks quantity calculation */

            var price_by_week  = $('.oe_price span.oe_currency_value').html()
                quantity = parseInt(weeks)
                price_total = 0

            price_by_week = parseFloat(price_by_week.replace(',', '.'));

            if(quantity > 3){
                quantity = 3 // 4th week is free
                price_total = price_by_week * quantity
            }else{
                price_total = price_by_week * quantity
            }

            $('input[name="add_qty"]').val(quantity);

            if(price_total){

                price_total = price_total.toFixed(2);
                price_total = price_total.replace('.', ',');

                /* sale_rental fields */
                var number_of_days = Math.abs((weeks * 7) + 1);

                $('input[name="number_of_days"]').val(number_of_days)
                $('input[name="start_date"]').val(start_date)
                $('input[name="end_date"]').val(parse_end_date)

                /* show "add to cart" button and price */
                $('span.dates-total-price').html(price_total);
                $('.form-control-dates-total').show();
                $('a#add_to_cart').show();
            }
        }
    }
    $('input[name="start-date"]').on('change', function(){
        calcDates();
    });
    /*$('input[name="end-date"]').on('change', function(){
        calcDates();
    });*/
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
