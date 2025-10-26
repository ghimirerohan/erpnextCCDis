// custom_erp/public/js/nepali_date_patch.js
// Monkey-patch frappe.ui.form.ControlDate and ControlDatetime to use Nepali calendar

frappe.provide('custom_erp.nepali.patch');

(function() {
    // Function to apply Nepali date controls
    function applyNepaliControls() {
        // Check if Nepali calendar is enabled via boot settings
        var nepaliCalendarEnabled = frappe.boot && frappe.boot.enable_nepali_calendar;
        
        if (!nepaliCalendarEnabled) {
            console.log('custom_erp: Nepali calendar is disabled.');
            return; // nothing to do
        }

        // Ensure the Nepali library exists
        if (!window.NepaliFunctions) {
            console.warn('NepaliFunctions not found. Make sure nepali datepicker is loaded.');
            return;
        }

        // Ensure frappe.ui.form exists
        if (!frappe.ui || !frappe.ui.form || !frappe.ui.form.ControlDate) {
            console.warn('Frappe form controls not yet loaded.');
            return;
        }

        console.log('custom_erp: Applying Nepali date controls...');

        // Keep originals for fallback
        var OriginalDate = frappe.ui.form.ControlDate;
        var OriginalDatetime = frappe.ui.form.ControlDatetime;

        // ============================================================
        // Nepali Date Control
        // ============================================================
        class NepaliDateControl extends OriginalDate {
            make_input() {
                var me = this;
                
                // Flag to prevent recursive value setting
                this._is_setting_value = false;
                
                // Call parent but DON'T let it set up datepicker
                // by temporarily setting a flag
                this._skip_datepicker = true;
                super.make_input();
                this._skip_datepicker = false;
                
                // Force input to be visible and accessible
                if (this.$input) {
                    this.$input.attr('type', 'text');
                    this.$input.removeAttr('hidden');
                    this.$input.css({
                        'display': 'block',
                        'visibility': 'visible',
                        'opacity': '1',
                        'height': 'auto',
                        'width': 'auto'
                    });
                    this.$input.show();
                }
                
                // Ensure wrapper is visible
                if (this.$input_wrapper) {
                    this.$input_wrapper.css({
                        'display': 'block',
                        'visibility': 'visible'
                    });
                    this.$input_wrapper.show();
                }
                
                // Ensure the whole control wrapper is visible
                if (this.$wrapper) {
                    this.$wrapper.css({
                        'display': 'block',
                        'visibility': 'visible'
                    });
                    this.$wrapper.show();
                    this.$wrapper.find('.datepicker-icon').remove();
                }
                
                // Remove any datepicker that was created
                if (this.datepicker) {
                    try {
                        this.datepicker.destroy();
                    } catch (e) {}
                    this.datepicker = null;
                }
                
                // Set placeholder
                try {
                    var todayBs = custom_erp.nepali.getTodayBs();
                    if (todayBs) this.$input.attr('placeholder', todayBs);
                } catch (e) {}

                // Initialize NepaliDatePicker
                try {
                    custom_erp.nepali.initNepaliPicker(this.$input, {
                        ndpYear: true,
                        ndpMonth: true,
                        onChange: function(e) {
                            if (me._is_setting_value) return;
                            var bsVal = e.bs;
                            if (!bsVal) return;
                            
                            try {
                                var ad = custom_erp.nepali.bsToAd(bsVal);
                                if (ad) {
                                    me._is_setting_value = true;
                                    me.set_model_value(ad);
                                    me._is_setting_value = false;
                                }
                            } catch (err) {
                                console.error("Conversion BS→AD failed:", err);
                            }
                        }
                    });
                } catch (e) {
                    console.error('Failed to initialize Nepali picker', e);
                }
            }
            
            // Override setup_datepicker to prevent Frappe's datepicker
            setup_datepicker() {
                // Do nothing - we use Nepali picker instead
                // This prevents Frappe from setting up its datepicker
            }

            // When programmatically setting the value (AD), render as BS in input
            set_formatted_input(value) {
                if (!value) {
                    this.$input && this.$input.val("");
                    return;
                }
                
                try {
                    var bs = custom_erp.nepali.adToBs(value);
                    if (bs) {
                        this.$input && this.$input.val(bs);
                        return;
                    }
                } catch (err) {
                    console.error("Conversion AD→BS failed:", err);
                }
                
                // Fallback to default behavior
                super.set_formatted_input(value);
            }

            // Parse user input (BS) to AD for storage
            parse(value) {
                if (!value || value === '') return '';
                
                // Handle "Today" shortcut
                if (value.toLowerCase() === "today") {
                    var todayAd = frappe.datetime.now_date();
                    return todayAd;
                }
                
                try {
                    // If it's already in AD format (YYYY-MM-DD), return as is
                    if (/^\d{4}-\d{2}-\d{2}$/.test(value)) {
                        // Try to parse as BS first, fallback to AD
                        try {
                            var testBs = custom_erp.nepali.bsToAd(value);
                            if (testBs) return testBs;
                        } catch (e) {
                            // If BS parsing fails, assume it's AD
                            return value;
                        }
                    }
                    
                    // Try to convert from BS to AD
                    return custom_erp.nepali.bsToAd(value);
                } catch (err) {
                    console.error("Parsing failed:", err);
                    return value;
                }
            }
        }

        // ============================================================
        // Nepali Datetime Control
        // ============================================================
        class NepaliDatetimeControl extends OriginalDatetime {
            make_input() {
                var me = this;
                
                // Flag to prevent recursive value setting
                this._is_setting_value = false;
                
                // Call parent but skip datepicker
                this._skip_datepicker = true;
                super.make_input();
                this._skip_datepicker = false;
                
                // Force all inputs to be visible
                if (this.$input) {
                    this.$input.attr('type', 'text');
                    this.$input.removeAttr('hidden');
                    this.$input.css({
                        'display': 'block',
                        'visibility': 'visible',
                        'opacity': '1'
                    });
                    this.$input.show();
                }
                
                if (this.$input_wrapper) {
                    this.$input_wrapper.css({
                        'display': 'block',
                        'visibility': 'visible'
                    });
                    this.$input_wrapper.show();
                }
                
                if (this.$wrapper) {
                    this.$wrapper.css({
                        'display': 'block',
                        'visibility': 'visible'
                    });
                    this.$wrapper.show();
                    this.$wrapper.find('.datepicker-icon').remove();
                }
                
                // Remove any datepicker
                if (this.datepicker) {
                    try {
                        this.datepicker.destroy();
                    } catch (e) {}
                    this.datepicker = null;
                }
                
                // Find the date input
                var $dateInput = this.$input;
                if (this.$input_wrapper) {
                    var dateInputEl = this.$input_wrapper.find('input[data-fieldtype="Date"]');
                    if (dateInputEl.length > 0) {
                        $dateInput = dateInputEl;
                    }
                }
                
                if ($dateInput) {
                    $dateInput.attr('type', 'text');
                    $dateInput.css({
                        'display': 'block',
                        'visibility': 'visible'
                    });
                    $dateInput.show();
                }

                // Initialize NepaliDatePicker
                try {
                    custom_erp.nepali.initNepaliPicker($dateInput, {
                        ndpYear: true,
                        ndpMonth: true,
                        onChange: function(e) {
                            if (me._is_setting_value) return;
                            var bsVal = e.bs;
                            if (!bsVal) return;
                            
                            try {
                                var ad = custom_erp.nepali.bsToAd(bsVal);
                                if (ad) {
                                    var currentVal = me.get_value();
                                    var timePart = '';
                                    
                                    if (currentVal && currentVal.indexOf(' ') > -1) {
                                        timePart = currentVal.split(' ').slice(1).join(' ');
                                    }
                                    
                                    var newVal = ad + (timePart ? (' ' + timePart) : '');
                                    
                                    me._is_setting_value = true;
                                    me.set_model_value(newVal);
                                    me._is_setting_value = false;
                                }
                            } catch (err) {
                                console.error("Conversion BS→AD failed:", err);
                            }
                        }
                    });
                } catch (e) {
                    console.error('Failed to initialize Nepali picker on datetime', e);
                }
            }
            
            // Override setup_datepicker to prevent Frappe's datepicker
            setup_datepicker() {
                // Do nothing - we use Nepali picker instead
            }

            // When programmatically setting the value (AD datetime), render date as BS
            set_formatted_input(value) {
                if (!value) {
                    this.$input && this.$input.val("");
                    return;
                }
                
                try {
                    // Split date and time
                    var parts = value.split(' ');
                    var adDate = parts[0];
                    var timePart = parts.slice(1).join(' ');
                    
                    var bs = custom_erp.nepali.adToBs(adDate);
                    if (bs) {
                        var displayValue = bs + (timePart ? (' ' + timePart) : '');
                        this.$input && this.$input.val(displayValue);
                        return;
                    }
                } catch (err) {
                    console.error("Conversion AD→BS failed:", err);
                }
                
                // Fallback to default behavior
                super.set_formatted_input(value);
            }

            // Parse user input (BS datetime) to AD datetime for storage
            parse(value) {
                if (!value || value === '') return '';
                
                // Handle "Now" shortcut
                if (value.toLowerCase() === "now") {
                    return frappe.datetime.now_datetime();
                }
                
                try {
                    // Split date and time portions
                    var parts = value.split(' ');
                    var bsDate = parts[0];
                    var timePart = parts.slice(1).join(' ');
                    
                    // Convert date portion from BS to AD
                    var adDate = custom_erp.nepali.bsToAd(bsDate);
                    if (adDate) {
                        return adDate + (timePart ? (' ' + timePart) : '');
                    }
                    
                    return value;
                } catch (err) {
                    console.error("Datetime parsing failed:", err);
                    return value;
                }
            }
        }

        // ============================================================
        // Apply the overrides globally
        // ============================================================
        frappe.ui.form.ControlDate = NepaliDateControl;
        frappe.ui.form.ControlDatetime = NepaliDatetimeControl;

        console.log('custom_erp: Nepali date controls applied successfully (UI only).');
    }

    // Apply controls when frappe is ready
    if (frappe && frappe.boot) {
        // If frappe is already loaded, apply immediately
        applyNepaliControls();
    } else {
        // Otherwise wait for frappe-ready event
        $(document).on('frappe-ready', function() {
            applyNepaliControls();
        });
    }
})();

