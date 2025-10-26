// custom_erp/public/js/nepali_date_adapter.js
// Conversion adapter for Nepali dates using NepaliFunctions library

frappe.provide('custom_erp.nepali');

custom_erp.nepali = (function() {
    // Ensure NepaliFunctions library is present
    
    /**
     * Convert AD (Gregorian) date to BS (Nepali) date
     * @param {string} adDateStr - Date in YYYY-MM-DD format
     * @returns {string} BS date in YYYY-MM-DD format
     */
    function adToBs(adDateStr) {
        if (!window.NepaliFunctions || !adDateStr) return '';
        try {
            // NepaliFunctions.AD2BS returns BS date in YYYY-MM-DD format by default
            return NepaliFunctions.AD2BS(adDateStr);
        } catch (e) {
            console.error('AD2BS conversion failed', e, adDateStr);
            return '';
        }
    }

    /**
     * Convert BS (Nepali) date to AD (Gregorian) date
     * @param {string} bsDateStr - Date in YYYY-MM-DD format
     * @returns {string} AD date in YYYY-MM-DD format
     */
    function bsToAd(bsDateStr) {
        if (!window.NepaliFunctions || !bsDateStr) return '';
        try {
            // NepaliFunctions.BS2AD returns AD date in YYYY-MM-DD format by default
            return NepaliFunctions.BS2AD(bsDateStr);
        } catch (e) {
            console.error('BS2AD conversion failed', e, bsDateStr);
            return '';
        }
    }

    /**
     * Initialize Nepali Date Picker on an input element
     * @param {jQuery|HTMLElement} $input - Input element or jQuery object
     * @param {Object} opts - Options for the date picker
     */
    function initNepaliPicker($input, opts) {
        // Ensure we have a jQuery object
        var $el = $input.jquery ? $input : $($input);
        
        if (!$el || $el.length === 0) {
            console.warn('Nepali DatePicker: Invalid input element');
            return;
        }

        // Check if nepaliDatePicker jQuery plugin is available
        if (typeof $el.nepaliDatePicker !== 'function') {
            console.warn('Nepali DatePicker plugin not loaded. Ensure nepali.datepicker.v5.0.6.min.js is included.');
            return;
        }

        try {
            // Initialize the NepaliDatePicker on the element with default options
            var defaultOpts = {
                ndpYear: true,
                ndpMonth: true,
                ndpFormat: 'YYYY-MM-DD',
                closeOnDateSelect: true,
                miniEnglishDates: true,  // Mini English Date format
                mode: 'dark'
            };
            
            // Merge user options with defaults
            var finalOpts = $.extend({}, defaultOpts, opts || {});
            
            $el.nepaliDatePicker(finalOpts);
        } catch (e) {
            console.error('Failed to initialize NepaliDatePicker', e);
        }
    }

    /**
     * Get today's date in BS format
     * @returns {string} Today's BS date in YYYY-MM-DD format
     */
    function getTodayBs() {
        if (!window.NepaliFunctions) return '';
        try {
            var todayAd = frappe.datetime.now_date(); // YYYY-MM-DD
            return adToBs(todayAd);
        } catch (e) {
            console.error('Failed to get today BS date', e);
            return '';
        }
    }

    // Public API
    return {
        adToBs: adToBs,
        bsToAd: bsToAd,
        initNepaliPicker: initNepaliPicker,
        getTodayBs: getTodayBs
    };
})();

