odoo.define('website_quote.website_quote', function (require) {
    'use strict';

    var ajax = require('web.ajax');
    var Widget = require('web.Widget');
    var website = require('website.website');

    if(!$('.o_website_rental').length) {
        return $.Deferred().reject("DOM doesn't contain '.o_website_rental'");
}

    // Add to SO button
    var UpdateLineButton = Widget.extend({
        events: {
            'click' : 'onClick',
        },
        /**
         * @override
         */
        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.elems = self._getUpdatableElements();
                self.elems.$lineQuantity.change(function (ev) {
                    var quantity = parseInt(this.value);
                    self._onChangeQuantity(quantity);
                });
            });
        },
        /**
         * Process the change in line quantity
         *
         * @private
         * @param {Int} quantity, the new quantity of the line
         *    If not present it will increment/decrement the existing quantity
         */
        _onChangeQuantity: function (quantity) {
            var href = this.$el.attr("href");
            var order_id = href.match(/order_id=([0-9]+)/)[1];
            var line_id = href.match(/update_line(_dict)?\/([0-9]+)/)[2];
            var token = href.match(/token=([\w\d-]*)/)[1];

            var callParams = {
                'line_id': parseInt(line_id),
                'order_id': parseInt(order_id),
                'token': token,
                'remove': this.$el.is('[href*="remove"]'),
                'unlink': this.$el.is('[href*="unlink"]'),
                'input_quantity': quantity >= 0 ? quantity : false,
            };
            this._callUpdateLineRoute(callParams).then(this._updateOrderValues.bind(this));
            return false;
        },
        /**
         * Reacts to the click on the -/+ buttons
         *
         * @param {Event} ev
         */
        onClick: function (ev) {
            ev.preventDefault();
            return this._onChangeQuantity();
        },
        /**
         * Calls the route to get updated values of the line and order
         * when the quantity of a product has changed
         *
         * @private
         * @param {Object} params
         * @return {Deferred}
         */
        _callUpdateLineRoute: function (params) {
            var def = new $.Deferred();
            ajax.jsonRpc("/quote/update_line_dict", 'call', params)
                .then(def.resolve.bind(def))
                .fail(function () {
                    // Compatibility: the server may not have been restarted
                    // So the real route may not exist
                    delete params.input_quantity;
                    ajax.jsonRpc("/quote/update_line", 'call', params)
                        .fail(def.reject.bind(def))
                        .then(function (data) {
                            // Data is an array, convert it to a dict
                            var actualData = data;
                            if (data) {
                                actualData = {
                                    order_amount_total: data[1],
                                    order_line_product_uom_qty: data[0],
                                };
                            }
                            def.resolve(actualData);
                        });
                });
            return def;
        },
        /**
         * Processes data from the server to update the UI
         *
         * @private
         * @param {Object} data: contains order and line updated values
         */
        _updateOrderValues: function (data) {
            if (!data) {
                window.location.reload();
            }

            var orderAmountTotal = data.order_amount_total;
            var orderAmountUntaxed = data.order_amount_untaxed;
            var orderAmountTax = data.order_amount_tax;

            var lineProductUomQty = data.order_line_product_uom_qty;
            var linePriceTotal = data.order_line_price_total;
            var linePriceSubTotal = data.order_line_price_subtotal;

            this.elems.$lineQuantity.val(lineProductUomQty)

            if (this.elems.$linePriceTotal.length && linePriceTotal !== undefined) {
                this.elems.$linePriceTotal.text(linePriceTotal);
            }
            if (this.elems.$linePriceSubTotal.length && linePriceSubTotal !== undefined) {
                this.elems.$linePriceSubTotal.text(linePriceSubTotal);
            }

            if (orderAmountUntaxed !== undefined) {
                this.elems.$orderAmountUntaxed.text(orderAmountUntaxed);
            }

            if (orderAmountTax !== undefined) {
                this.elems.$orderAmountTax.text(orderAmountTax);
            }

            if (orderAmountTotal !== undefined) {
                this.elems.$orderAmountTotal.text(orderAmountTotal);
            }
        },
        /**
         * Locate in the DOM the elements to update
         * Mostly for compatibility, when the module has not been upgraded
         * In that case, we need to fall back to some other elements
         *
         * @private
         * @return {Object}: Jquery elements to update
         */
        _getUpdatableElements: function () {
            var $parentTr = this.$el.parents('tr:first');
            var $linePriceTotal = $parentTr.find('.oe_order_line_price_total .oe_currency_value');
            var $linePriceSubTotal = $parentTr.find('.oe_order_line_price_subtotal .oe_currency_value');

            if (!$linePriceTotal.length && !$linePriceSubTotal.length) {
                $linePriceTotal = $linePriceSubTotal = $parentTr.find('.oe_currency_value').last();
            }

            var $orderAmountUntaxed = $('[data-id="total_untaxed"]>span');
            var $orderAmountTax = $('[data-id="total_taxes"]>span');
            var $orderAmountTotal = $('[data-id="total_amount"]>span');

            if (!$orderAmountUntaxed.length && !$orderAmountTax.length) {
                $orderAmountUntaxed = $orderAmountTotal.eq(1);
                $orderAmountTax = $orderAmountTotal.eq(2);
                $orderAmountTotal = $orderAmountTotal.eq(0).add($orderAmountTotal.eq(3));
            }

            return {
                $lineQuantity: this.$el.parents('.input-group:first').find('.js_quantity'),
                $linePriceSubTotal: $linePriceSubTotal,
                $linePriceTotal: $linePriceTotal,
                $orderAmountUntaxed: $orderAmountUntaxed,
                $orderAmountTax: $orderAmountTax,
                $orderAmountTotal: $orderAmountTotal,
            }
        }
    });

    var update_button_list = [];
    $('a.js_update_line_json').each(function( index ) {
        var button = new UpdateLineButton();
        button.setElement($(this)).start();
        update_button_list.push(button);
    });

    // Accept Modal, with jSignature
    var AcceptModal = Widget.extend({
        events: {
            'shown.bs.modal': 'initSignature',
            'click #sign_clean': 'clearSignature',
            'submit #rental_agreement': 'submitForm',
        },
        initSignature: function(ev){
            this.$("#signature").empty().jSignature({'decor-color' : '#D1D0CE', 'color': '#000', 'background-color': '#fff'});
            this.empty_sign = this.$("#signature").jSignature("getData",'image');
        },
        clearSignature: function(ev){
            this.$("#signature").jSignature('reset');
        },
        submitForm: function(ev){
            // extract data
            var self = this;
            var $confirm_btn = self.$el.find('button[type="submit"]');
            var order_id = self.$el.find('form').data("order-id");
            ev.preventDefault();
            var signer_name = self.$("#name").val();
            var signature = self.$("#signature").jSignature("getData",'image');
            var is_empty = signature ? this.empty_sign[1] == signature[1] : false;
            self.$('#signer').toggleClass('has-error', !signer_name);
            self.$('#drawsign').toggleClass('panel-danger', is_empty).toggleClass('panel-default', !is_empty);
            if (is_empty || ! signer_name){
                setTimeout(function () {
                    self.$('button[type="submit"], a.a-submit').removeAttr('data-loading-text').button('reset');
                })
                return false;
            }
            $confirm_btn.prepend('<i class="fa fa-spinner fa-spin"></i> ');
            $confirm_btn.attr('disabled', true);
            ajax.jsonRpc("/order/rental_agreement", 'call', {
                'order_id': order_id,
                'signer': signer_name,
                'sign': signature?JSON.stringify(signature[1]):false,
            }).then(function (data) {
                var message_id = (data) ? 3 : 4;
                self.$el.modal('hide');
            });
            return false;
        },
    });

    var accept_modal = new AcceptModal();
    accept_modal.setElement($('#modalaccept'));
    accept_modal.start();
});
