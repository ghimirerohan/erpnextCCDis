frappe.ui.form.ControlDate = class CustomNepaliDate extends frappe.ui.form.ControlData {
  make() {
    super.make();
    this._is_setting_value = false;
    this.setup_nepali_date_picker();
  }

  make_input() {
    super.make_input();
    this.setup_nepali_date_picker();
  }

  setup_nepali_date_picker() {
    if (!this.$input) return;  // ensure input exists

    if (this.datepicker) {
      this.datepicker.destroy();
      this.datepicker = null;
    }
    this.$wrapper.find(".datepicker-icon").remove();
    this.$input.attr("type", "text");

    this.$input.nepaliDatePicker({
      ndpYear: true,
      ndpMonth: true,
      ndpFormat: 'YYYY-MM-DD',
      closeOnDateSelect: true,
      miniEnglishDates: true,
      mode: 'dark',
      onChange: (e) => {
        if (this._is_setting_value) return;
        const bs_date = e.bs;
        try {
          const ad = NepaliFunctions.BS2AD(bs_date);
          this._is_setting_value = true;
          this.set_value(ad);
          this._is_setting_value = false;
        } catch (err) {
          console.error("Conversion BS→AD failed:", err);
        }
      }
    });

    if (this.value) {
      this.set_formatted_input(this.value);
    }
  }

  set_formatted_input(value) {
    if (!value) {
      return this.$input?.val("");
    }
    try {
      const bs = NepaliFunctions.AD2BS(value);
      this.$input?.val(bs);
    } catch (err) {
      console.error("Conversion AD→BS failed:", err);
      this.$input?.val(value);
    }
  }

  set_value(value) {
    super.set_value(value);
    this.set_formatted_input(value);
  }

  parse(value) {
    if (!value || value === '') return '';
    if (value === "Today") {
      return NepaliFunctions.BS2AD(NepaliFunctions.getToday());
    }
    try {
      if (/^\d{4}-\d{2}-\d{2}$/.test(value)) {
        return value;
      }
      return NepaliFunctions.BS2AD(value);
    } catch (err) {
      console.error("Parsing failed:", err);
      return value;
    }
  }
};
