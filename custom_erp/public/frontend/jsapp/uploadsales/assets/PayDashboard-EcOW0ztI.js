var __async = (__this, __arguments, generator) => {
  return new Promise((resolve, reject) => {
    var fulfilled = (value) => {
      try {
        step(generator.next(value));
      } catch (e) {
        reject(e);
      }
    };
    var rejected = (value) => {
      try {
        step(generator.throw(value));
      } catch (e) {
        reject(e);
      }
    };
    var step = (x) => x.done ? resolve(x.value) : Promise.resolve(x.value).then(fulfilled, rejected);
    step((generator = generator.apply(__this, __arguments)).next());
  });
};
import { g as ref, c as computed, l as watch, k as onMounted, a as createElementBlock, b as createBaseVNode, ad as createStaticVNode, L as unref, t as toDisplayString, e as createCommentVNode, I as createTextVNode, F as Fragment, M as renderList, B as withDirectives, am as vModelSelect, z as createVNode, n as normalizeClass, o as openBlock } from "./vendor-BMb8bgkN.js";
import { j as _export_sfc, c as createResource, k as _sfc_main$1 } from "./ui-Ca38NmEL.js";
import { s as session } from "./index-Bgu5Yqv3.js";
const _hoisted_1 = { class: "min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50" };
const _hoisted_2 = { class: "bg-white shadow-sm border-b border-gray-200 sticky top-0 z-20" };
const _hoisted_3 = { class: "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8" };
const _hoisted_4 = { class: "flex justify-between items-center py-4 sm:py-6" };
const _hoisted_5 = { class: "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 space-y-6 sm:space-y-8" };
const _hoisted_6 = { class: "bg-white rounded-xl shadow-lg border border-gray-200 p-6 sm:p-8" };
const _hoisted_7 = { class: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 sm:gap-6" };
const _hoisted_8 = { class: "space-y-2" };
const _hoisted_9 = { class: "text-xl sm:text-2xl font-bold text-gray-900" };
const _hoisted_10 = { class: "text-sm sm:text-base text-gray-700" };
const _hoisted_11 = { class: "font-medium" };
const _hoisted_12 = { class: "flex-1 sm:text-center space-y-2 lg:max-w-md lg:mx-auto" };
const _hoisted_13 = { class: "text-2xl sm:text-3xl lg:text-4xl font-bold text-blue-600" };
const _hoisted_14 = { class: "text-sm text-gray-500" };
const _hoisted_15 = {
  key: 0,
  class: "pt-2 border-t border-gray-200"
};
const _hoisted_16 = { class: "text-lg sm:text-xl font-bold text-amber-600" };
const _hoisted_17 = { class: "flex flex-col gap-2" };
const _hoisted_18 = ["disabled"];
const _hoisted_19 = {
  key: 0,
  class: "animate-spin w-4 h-4 mr-2",
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor"
};
const _hoisted_20 = {
  key: 1,
  class: "w-4 h-4 mr-2",
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor"
};
const _hoisted_21 = ["disabled"];
const _hoisted_22 = {
  key: 0,
  class: "animate-spin w-4 h-4 mr-2",
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor"
};
const _hoisted_23 = {
  key: 1,
  class: "w-4 h-4 mr-2",
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor"
};
const _hoisted_24 = { class: "bg-white rounded-xl shadow-lg border border-gray-200 p-6 sm:p-8" };
const _hoisted_25 = { class: "space-y-4" };
const _hoisted_26 = { class: "flex flex-wrap gap-2" };
const _hoisted_27 = ["onClick"];
const _hoisted_28 = { class: "grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 border-t border-gray-200" };
const _hoisted_29 = ["value"];
const _hoisted_30 = { class: "customer-select-wrapper" };
const _hoisted_31 = { class: "relative" };
const _hoisted_32 = {
  key: 0,
  class: "pt-2 border-t border-gray-200"
};
const _hoisted_33 = { class: "flex flex-wrap gap-2" };
const _hoisted_34 = {
  key: 0,
  class: "inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
};
const _hoisted_35 = {
  key: 1,
  class: "inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800"
};
const _hoisted_36 = { class: "flex items-start gap-3" };
const _hoisted_37 = {
  key: 0,
  class: "flex-shrink-0"
};
const _hoisted_38 = {
  key: 1,
  class: "flex-shrink-0"
};
const _hoisted_39 = { class: "flex-1" };
const _hoisted_40 = { key: 0 };
const _hoisted_41 = {
  key: 0,
  class: "font-semibold"
};
const _hoisted_42 = { class: "bg-white rounded-xl shadow-lg border border-gray-200 p-6 sm:p-8" };
const _hoisted_43 = {
  key: 0,
  class: "text-center py-12"
};
const _hoisted_44 = {
  key: 1,
  class: "text-center py-12"
};
const _hoisted_45 = { key: 2 };
const _hoisted_46 = { class: "space-y-3" };
const _hoisted_47 = { class: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3" };
const _hoisted_48 = { class: "flex-1" };
const _hoisted_49 = { class: "flex items-center gap-2" };
const _hoisted_50 = { class: "text-base sm:text-lg font-semibold text-gray-900" };
const _hoisted_51 = {
  key: 0,
  class: "px-2 py-0.5 text-xs font-medium bg-blue-600 text-white rounded"
};
const _hoisted_52 = { class: "text-xs sm:text-sm text-gray-600 mt-1" };
const _hoisted_53 = { class: "text-xs text-gray-500 mt-1" };
const _hoisted_54 = { class: "text-right" };
const _hoisted_55 = { class: "text-xl sm:text-2xl font-bold text-blue-600" };
const _hoisted_56 = { key: 3 };
const _hoisted_57 = { class: "space-y-3" };
const _hoisted_58 = { class: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3" };
const _hoisted_59 = { class: "flex-1" };
const _hoisted_60 = { class: "text-base sm:text-lg font-semibold text-gray-900" };
const _hoisted_61 = { class: "text-xs sm:text-sm text-gray-600 mt-1" };
const _hoisted_62 = { class: "text-xs text-gray-500 mt-1" };
const _hoisted_63 = { class: "text-right" };
const _hoisted_64 = { class: "text-xl sm:text-2xl font-bold text-green-600" };
const _hoisted_65 = { key: 4 };
const _hoisted_66 = { class: "overflow-x-auto" };
const _hoisted_67 = { class: "min-w-full space-y-3" };
const _hoisted_68 = { class: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4" };
const _hoisted_69 = { class: "text-lg font-bold text-blue-600" };
const _hoisted_70 = { class: "text-sm font-medium text-gray-900" };
const _hoisted_71 = { class: "text-xs text-gray-600" };
const _hoisted_72 = { class: "text-sm font-medium text-gray-900" };
const _hoisted_73 = { class: "text-xs text-gray-600" };
const _hoisted_74 = { class: "text-sm font-medium text-gray-900" };
const _hoisted_75 = {
  key: 0,
  class: "text-xs text-blue-600 mt-1"
};
const _hoisted_76 = ["href"];
const _sfc_main = {
  __name: "PayDashboard",
  setup(__props) {
    const summary = ref({
      current_user: "",
      current_user_full_name: "",
      total_success_amount: 0,
      total_success_count: 0,
      unprocessed_count: 0
    });
    const bsToday = ref("");
    const adToday = (/* @__PURE__ */ new Date()).toISOString().slice(0, 10);
    const loading = ref(false);
    const loadingData = ref(false);
    const loadingCustomers = ref(false);
    const processingUnprocessed = ref(false);
    const processResult = ref(null);
    const viewModes = [
      { value: "username", label: "Username-wise" },
      { value: "customer", label: "Customer-wise" },
      { value: "transaction", label: "Transaction-wise" }
    ];
    const selectedViewMode = ref("username");
    const selectedUsername = ref("");
    const selectedCustomerValue = ref(null);
    const selectedCustomer = ref(null);
    const usernameOptions = ref([]);
    const customerOptions = ref([]);
    const usernameData = ref([]);
    const customerData = ref([]);
    const transactionData = ref([]);
    const summaryResource = createResource({
      url: "custom_erp.custom_erp.api.fonepay.get_pay_dashboard_summary",
      auto: false
    });
    const usernameGroupedResource = createResource({
      url: "custom_erp.custom_erp.api.fonepay.get_username_grouped_totals",
      auto: false
    });
    const customerGroupedResource = createResource({
      url: "custom_erp.custom_erp.api.fonepay.get_customer_grouped_totals",
      auto: false
    });
    const transactionListResource = createResource({
      url: "custom_erp.custom_erp.api.fonepay.get_transaction_list",
      auto: false
    });
    const filterCustomersResource = createResource({
      url: "custom_erp.custom_erp.api.fonepay.get_filter_customers_today",
      auto: false
    });
    const filterUsernamesResource = createResource({
      url: "custom_erp.custom_erp.api.fonepay.get_filter_usernames_today",
      auto: false
    });
    const unprocessedCountResource = createResource({
      url: "custom_erp.custom_erp.api.fonepay.get_today_unprocessed_count",
      auto: false
    });
    const processAllResource = createResource({
      url: "custom_erp.custom_erp.api.fonepay.process_all_today_unprocessed",
      auto: false
    });
    const hasActiveFilters = computed(() => {
      return Boolean(selectedUsername.value || selectedCustomer.value);
    });
    const hasData = computed(() => {
      if (selectedViewMode.value === "username") return usernameData.value.length > 0;
      if (selectedViewMode.value === "customer") return customerData.value.length > 0;
      if (selectedViewMode.value === "transaction") return transactionData.value.length > 0;
      return false;
    });
    const formatAmount = (amount) => {
      const num = Number(amount) || 0;
      return num.toLocaleString("en-IN", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    };
    const formatDateTime = (dateTime) => {
      if (!dateTime) return "—";
      const d = new Date(dateTime);
      return d.toLocaleString("en-IN", {
        hour: "2-digit",
        minute: "2-digit",
        day: "2-digit",
        month: "2-digit",
        year: "numeric"
      });
    };
    const getUsernameLabel = (username) => {
      const user = usernameOptions.value.find((u) => u.value === username);
      return user ? user.label : username;
    };
    const clearUsernameFilter = () => {
      selectedUsername.value = "";
      applyFilters();
    };
    const clearCustomerFilter = () => {
      selectedCustomerValue.value = null;
      selectedCustomer.value = null;
      applyFilters();
    };
    const loadSummary = () => __async(this, null, function* () {
      try {
        const [summaryRes, unprocessedRes] = yield Promise.all([
          summaryResource.fetch(),
          unprocessedCountResource.fetch()
        ]);
        summary.value = {
          current_user: (summaryRes == null ? void 0 : summaryRes.current_user) || session.user,
          current_user_full_name: (summaryRes == null ? void 0 : summaryRes.current_user_full_name) || session.user,
          total_success_amount: Number((summaryRes == null ? void 0 : summaryRes.total_success_amount) || 0),
          total_success_count: Number((summaryRes == null ? void 0 : summaryRes.total_success_count) || 0),
          unprocessed_count: Number((unprocessedRes == null ? void 0 : unprocessedRes.unprocessed_count) || 0)
        };
      } catch (error) {
        console.error("Failed to load summary", error);
      }
    });
    const loadUsernameData = () => __async(this, null, function* () {
      loadingData.value = true;
      try {
        const res = yield usernameGroupedResource.fetch({
          username_filter: selectedUsername.value || void 0
        });
        usernameData.value = (res == null ? void 0 : res.grouped_totals) || [];
      } catch (error) {
        console.error("Failed to load username data", error);
        usernameData.value = [];
      } finally {
        loadingData.value = false;
      }
    });
    const loadCustomerData = () => __async(this, null, function* () {
      var _a;
      loadingData.value = true;
      try {
        const res = yield customerGroupedResource.fetch({
          customer_filter: ((_a = selectedCustomer.value) == null ? void 0 : _a.value) || void 0,
          username_filter: selectedUsername.value || void 0
        });
        customerData.value = (res == null ? void 0 : res.grouped_totals) || [];
      } catch (error) {
        console.error("Failed to load customer data", error);
        customerData.value = [];
      } finally {
        loadingData.value = false;
      }
    });
    const loadTransactionData = () => __async(this, null, function* () {
      var _a;
      loadingData.value = true;
      try {
        const res = yield transactionListResource.fetch({
          username_filter: selectedUsername.value || void 0,
          customer_filter: ((_a = selectedCustomer.value) == null ? void 0 : _a.value) || void 0,
          limit: 100
        });
        transactionData.value = (res == null ? void 0 : res.transactions) || [];
      } catch (error) {
        console.error("Failed to load transaction data", error);
        transactionData.value = [];
      } finally {
        loadingData.value = false;
      }
    });
    const loadFilterOptions = () => __async(this, null, function* () {
      try {
        const [customersRes, usernamesRes] = yield Promise.all([
          filterCustomersResource.fetch(),
          filterUsernamesResource.fetch()
        ]);
        customerOptions.value = ((customersRes == null ? void 0 : customersRes.customers) || []).map((c) => ({
          label: c.label,
          value: c.value,
          customer_name: c.customer_name
        }));
        usernameOptions.value = (usernamesRes == null ? void 0 : usernamesRes.usernames) || [];
      } catch (error) {
        console.error("Failed to load filter options", error);
      }
    });
    const applyFilters = () => __async(this, null, function* () {
      if (selectedViewMode.value === "username") {
        yield loadUsernameData();
      } else if (selectedViewMode.value === "customer") {
        yield loadCustomerData();
      } else if (selectedViewMode.value === "transaction") {
        yield loadTransactionData();
      }
    });
    const processAllUnprocessed = () => __async(this, null, function* () {
      if (processingUnprocessed.value || summary.value.unprocessed_count < 1) {
        return;
      }
      processingUnprocessed.value = true;
      processResult.value = null;
      try {
        const res = yield processAllResource.fetch();
        processResult.value = res;
        if ((res == null ? void 0 : res.success_count) > 0) {
          console.log(`Successfully processed ${res.success_count} transactions. Added NPR ${formatAmount(res.new_success_amount)}`);
        }
        yield refreshAll();
      } catch (error) {
        console.error("Failed to process unprocessed transactions", error);
        processResult.value = {
          error: error.message || "Failed to process transactions"
        };
      } finally {
        processingUnprocessed.value = false;
      }
    });
    const refreshAll = () => __async(this, null, function* () {
      loading.value = true;
      try {
        yield Promise.all([
          loadSummary(),
          loadFilterOptions(),
          applyFilters()
        ]);
      } finally {
        loading.value = false;
      }
    });
    const tryLoadNepaliScriptAndSetBSToday = () => __async(this, null, function* () {
      try {
        if (typeof window !== "undefined" && !window.NepaliFunctions) {
          const s = document.createElement("script");
          s.src = "/assets/custom_erp/lib/nepali.datepicker.v5.0.6.min.js";
          document.head.appendChild(s);
          yield new Promise((resolve) => {
            s.onload = resolve;
            s.onerror = resolve;
          });
        }
        if (typeof window !== "undefined" && window.NepaliFunctions) {
          const d = /* @__PURE__ */ new Date();
          const bs = window.NepaliFunctions.AD2BS({ year: d.getFullYear(), month: d.getMonth() + 1, day: d.getDate() });
          bsToday.value = `${bs.year}-${String(bs.month).padStart(2, "0")}-${String(bs.day).padStart(2, "0")}`;
        }
      } catch (e) {
        console.warn("Nepali date script failed to load", e);
      }
    });
    watch(selectedViewMode, () => __async(this, null, function* () {
      yield applyFilters();
    }));
    watch(selectedUsername, () => __async(this, null, function* () {
      yield applyFilters();
    }));
    watch(selectedCustomerValue, (newValue) => {
      if (!newValue) {
        selectedCustomer.value = null;
        return;
      }
      let option = null;
      if (typeof newValue === "object" && newValue !== null) {
        option = newValue;
      } else {
        option = customerOptions.value.find((opt) => opt.value === newValue);
      }
      if (option) {
        selectedCustomer.value = option;
        applyFilters();
      }
    });
    onMounted(() => __async(this, null, function* () {
      yield Promise.all([
        loadSummary(),
        loadFilterOptions(),
        tryLoadNepaliScriptAndSetBSToday()
      ]);
      yield applyFilters();
    }));
    return (_ctx, _cache) => {
      return openBlock(), createElementBlock("div", _hoisted_1, [
        createBaseVNode("header", _hoisted_2, [
          createBaseVNode("div", _hoisted_3, [
            createBaseVNode("div", _hoisted_4, [
              _cache[5] || (_cache[5] = createStaticVNode('<div class="flex items-center space-x-3 sm:space-x-4" data-v-9fc4a308><div class="flex items-center justify-center w-10 h-10 sm:w-12 sm:h-12 bg-blue-600 rounded-lg" data-v-9fc4a308><svg class="w-5 h-5 sm:w-6 sm:h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" data-v-9fc4a308><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" data-v-9fc4a308></path></svg></div><div data-v-9fc4a308><h1 class="text-xl sm:text-2xl font-bold text-gray-900" data-v-9fc4a308>Pay Dashboard</h1><p class="text-xs sm:text-sm text-gray-600" data-v-9fc4a308>Today&#39;s Fonepay QR Statistics</p></div></div>', 1)),
              createBaseVNode("button", {
                onClick: _cache[0] || (_cache[0] = ($event) => unref(session).logout.submit()),
                class: "inline-flex items-center px-3 py-2 sm:px-4 sm:py-2 border border-gray-300 rounded-md shadow-sm text-xs sm:text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              }, _cache[4] || (_cache[4] = [
                createBaseVNode("svg", {
                  class: "w-4 h-4 mr-1 sm:mr-2",
                  fill: "none",
                  stroke: "currentColor",
                  viewBox: "0 0 24 24"
                }, [
                  createBaseVNode("path", {
                    "stroke-linecap": "round",
                    "stroke-linejoin": "round",
                    "stroke-width": "2",
                    d: "M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                  })
                ], -1),
                createBaseVNode("span", { class: "hidden sm:inline" }, "Logout", -1)
              ]))
            ])
          ])
        ]),
        createBaseVNode("main", _hoisted_5, [
          createBaseVNode("section", _hoisted_6, [
            createBaseVNode("div", _hoisted_7, [
              createBaseVNode("div", _hoisted_8, [
                _cache[6] || (_cache[6] = createBaseVNode("div", { class: "text-xs sm:text-sm text-gray-500" }, "Today (BS)", -1)),
                createBaseVNode("div", _hoisted_9, toDisplayString(bsToday.value || unref(adToday)), 1),
                createBaseVNode("div", _hoisted_10, [
                  createBaseVNode("span", _hoisted_11, toDisplayString(summary.value.current_user_full_name || summary.value.current_user || unref(session).user), 1)
                ])
              ]),
              createBaseVNode("div", _hoisted_12, [
                _cache[8] || (_cache[8] = createBaseVNode("div", { class: "text-xs sm:text-sm uppercase text-gray-600 tracking-wide mb-2" }, "Today's Total Success", -1)),
                createBaseVNode("div", _hoisted_13, "NPR " + toDisplayString(formatAmount(summary.value.total_success_amount)), 1),
                createBaseVNode("div", _hoisted_14, toDisplayString(summary.value.total_success_count || 0) + " payments", 1),
                summary.value.unprocessed_count > 0 ? (openBlock(), createElementBlock("div", _hoisted_15, [
                  _cache[7] || (_cache[7] = createBaseVNode("div", { class: "text-xs text-amber-700 font-medium mb-1" }, "Unprocessed Transactions", -1)),
                  createBaseVNode("div", _hoisted_16, toDisplayString(summary.value.unprocessed_count), 1)
                ])) : createCommentVNode("", true)
              ]),
              createBaseVNode("div", _hoisted_17, [
                createBaseVNode("button", {
                  onClick: refreshAll,
                  disabled: loading.value || processingUnprocessed.value,
                  class: "inline-flex items-center justify-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg shadow hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 active:scale-95 transition"
                }, [
                  loading.value ? (openBlock(), createElementBlock("svg", _hoisted_19, _cache[9] || (_cache[9] = [
                    createBaseVNode("circle", {
                      cx: "12",
                      cy: "12",
                      r: "10",
                      "stroke-width": "4",
                      class: "opacity-25"
                    }, null, -1),
                    createBaseVNode("path", {
                      d: "M4 12a8 8 0 018-8",
                      "stroke-width": "4",
                      class: "opacity-75"
                    }, null, -1)
                  ]))) : (openBlock(), createElementBlock("svg", _hoisted_20, _cache[10] || (_cache[10] = [
                    createBaseVNode("path", {
                      "stroke-linecap": "round",
                      "stroke-linejoin": "round",
                      "stroke-width": "2",
                      d: "M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                    }, null, -1)
                  ]))),
                  _cache[11] || (_cache[11] = createTextVNode(" Refresh "))
                ], 8, _hoisted_18),
                summary.value.unprocessed_count >= 1 ? (openBlock(), createElementBlock("button", {
                  key: 0,
                  onClick: processAllUnprocessed,
                  disabled: processingUnprocessed.value || loading.value,
                  class: "inline-flex items-center justify-center px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-lg shadow hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 active:scale-95 transition"
                }, [
                  processingUnprocessed.value ? (openBlock(), createElementBlock("svg", _hoisted_22, _cache[12] || (_cache[12] = [
                    createBaseVNode("circle", {
                      cx: "12",
                      cy: "12",
                      r: "10",
                      "stroke-width": "4",
                      class: "opacity-25"
                    }, null, -1),
                    createBaseVNode("path", {
                      d: "M4 12a8 8 0 018-8",
                      "stroke-width": "4",
                      class: "opacity-75"
                    }, null, -1)
                  ]))) : (openBlock(), createElementBlock("svg", _hoisted_23, _cache[13] || (_cache[13] = [
                    createBaseVNode("path", {
                      "stroke-linecap": "round",
                      "stroke-linejoin": "round",
                      "stroke-width": "2",
                      d: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                    }, null, -1)
                  ]))),
                  createTextVNode(" Process All (" + toDisplayString(summary.value.unprocessed_count) + ") ", 1)
                ], 8, _hoisted_21)) : createCommentVNode("", true)
              ])
            ])
          ]),
          createBaseVNode("section", _hoisted_24, [
            createBaseVNode("div", _hoisted_25, [
              createBaseVNode("div", null, [
                _cache[14] || (_cache[14] = createBaseVNode("label", { class: "block text-sm font-semibold text-gray-700 mb-2" }, "View Mode", -1)),
                createBaseVNode("div", _hoisted_26, [
                  (openBlock(), createElementBlock(Fragment, null, renderList(viewModes, (mode) => {
                    return createBaseVNode("button", {
                      key: mode.value,
                      onClick: ($event) => selectedViewMode.value = mode.value,
                      class: normalizeClass([
                        "px-4 py-2 rounded-lg text-sm font-medium transition-all",
                        selectedViewMode.value === mode.value ? "bg-blue-600 text-white shadow-md" : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                      ])
                    }, toDisplayString(mode.label), 11, _hoisted_27);
                  }), 64))
                ])
              ]),
              createBaseVNode("div", _hoisted_28, [
                createBaseVNode("div", null, [
                  _cache[16] || (_cache[16] = createBaseVNode("label", { class: "block text-sm font-semibold text-gray-700 mb-2" }, "Filter by Username", -1)),
                  withDirectives(createBaseVNode("select", {
                    "onUpdate:modelValue": _cache[1] || (_cache[1] = ($event) => selectedUsername.value = $event),
                    onChange: applyFilters,
                    class: "w-full px-3 py-2 h-[44px] border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  }, [
                    _cache[15] || (_cache[15] = createBaseVNode("option", { value: "" }, "All Users", -1)),
                    (openBlock(true), createElementBlock(Fragment, null, renderList(usernameOptions.value, (user) => {
                      return openBlock(), createElementBlock("option", {
                        key: user.value,
                        value: user.value
                      }, toDisplayString(user.label), 9, _hoisted_29);
                    }), 128))
                  ], 544), [
                    [vModelSelect, selectedUsername.value]
                  ])
                ]),
                createBaseVNode("div", _hoisted_30, [
                  _cache[17] || (_cache[17] = createBaseVNode("label", { class: "block text-sm font-semibold text-gray-700 mb-2" }, "Filter by Customer", -1)),
                  createBaseVNode("div", _hoisted_31, [
                    createVNode(unref(_sfc_main$1), {
                      modelValue: selectedCustomerValue.value,
                      "onUpdate:modelValue": _cache[2] || (_cache[2] = ($event) => selectedCustomerValue.value = $event),
                      options: customerOptions.value,
                      loading: loadingCustomers.value,
                      placeholder: "Search customer by name or code",
                      class: "customer-autocomplete w-full text-sm"
                    }, null, 8, ["modelValue", "options", "loading"])
                  ])
                ])
              ]),
              hasActiveFilters.value ? (openBlock(), createElementBlock("div", _hoisted_32, [
                _cache[20] || (_cache[20] = createBaseVNode("div", { class: "text-xs font-medium text-gray-600 mb-2" }, "Active Filters:", -1)),
                createBaseVNode("div", _hoisted_33, [
                  selectedUsername.value ? (openBlock(), createElementBlock("span", _hoisted_34, [
                    createTextVNode(" User: " + toDisplayString(getUsernameLabel(selectedUsername.value)) + " ", 1),
                    createBaseVNode("button", {
                      onClick: clearUsernameFilter,
                      class: "ml-2 hover:text-blue-600"
                    }, _cache[18] || (_cache[18] = [
                      createBaseVNode("svg", {
                        class: "w-3 h-3",
                        fill: "none",
                        stroke: "currentColor",
                        viewBox: "0 0 24 24"
                      }, [
                        createBaseVNode("path", {
                          "stroke-linecap": "round",
                          "stroke-linejoin": "round",
                          "stroke-width": "2",
                          d: "M6 18L18 6M6 6l12 12"
                        })
                      ], -1)
                    ]))
                  ])) : createCommentVNode("", true),
                  selectedCustomer.value ? (openBlock(), createElementBlock("span", _hoisted_35, [
                    createTextVNode(" Customer: " + toDisplayString(selectedCustomer.value.customer_name || selectedCustomer.value.value) + " ", 1),
                    createBaseVNode("button", {
                      onClick: clearCustomerFilter,
                      class: "ml-2 hover:text-green-600"
                    }, _cache[19] || (_cache[19] = [
                      createBaseVNode("svg", {
                        class: "w-3 h-3",
                        fill: "none",
                        stroke: "currentColor",
                        viewBox: "0 0 24 24"
                      }, [
                        createBaseVNode("path", {
                          "stroke-linecap": "round",
                          "stroke-linejoin": "round",
                          "stroke-width": "2",
                          d: "M6 18L18 6M6 6l12 12"
                        })
                      ], -1)
                    ]))
                  ])) : createCommentVNode("", true)
                ])
              ])) : createCommentVNode("", true)
            ])
          ]),
          processResult.value && !processingUnprocessed.value ? (openBlock(), createElementBlock("section", {
            key: 0,
            class: normalizeClass(["bg-white rounded-xl shadow-lg border-2 p-6 sm:p-8", processResult.value.error ? "border-red-300 bg-red-50" : "border-green-300 bg-green-50"])
          }, [
            createBaseVNode("div", _hoisted_36, [
              processResult.value.error ? (openBlock(), createElementBlock("div", _hoisted_37, _cache[21] || (_cache[21] = [
                createBaseVNode("svg", {
                  class: "w-6 h-6 text-red-600",
                  fill: "none",
                  stroke: "currentColor",
                  viewBox: "0 0 24 24"
                }, [
                  createBaseVNode("path", {
                    "stroke-linecap": "round",
                    "stroke-linejoin": "round",
                    "stroke-width": "2",
                    d: "M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  })
                ], -1)
              ]))) : (openBlock(), createElementBlock("div", _hoisted_38, _cache[22] || (_cache[22] = [
                createBaseVNode("svg", {
                  class: "w-6 h-6 text-green-600",
                  fill: "none",
                  stroke: "currentColor",
                  viewBox: "0 0 24 24"
                }, [
                  createBaseVNode("path", {
                    "stroke-linecap": "round",
                    "stroke-linejoin": "round",
                    "stroke-width": "2",
                    d: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  })
                ], -1)
              ]))),
              createBaseVNode("div", _hoisted_39, [
                createBaseVNode("h4", {
                  class: normalizeClass(["font-semibold mb-2", processResult.value.error ? "text-red-800" : "text-green-800"])
                }, toDisplayString(processResult.value.error ? "Processing Error" : "Processing Complete"), 3),
                createBaseVNode("div", {
                  class: normalizeClass(["text-sm space-y-1", processResult.value.error ? "text-red-700" : "text-green-700"])
                }, [
                  processResult.value.error ? (openBlock(), createElementBlock("p", _hoisted_40, toDisplayString(processResult.value.error), 1)) : (openBlock(), createElementBlock(Fragment, { key: 1 }, [
                    createBaseVNode("p", null, [
                      createBaseVNode("strong", null, toDisplayString(processResult.value.processed_count), 1),
                      _cache[23] || (_cache[23] = createTextVNode(" transactions processed"))
                    ]),
                    createBaseVNode("p", null, [
                      createBaseVNode("strong", null, toDisplayString(processResult.value.success_count), 1),
                      _cache[24] || (_cache[24] = createTextVNode(" successful, ")),
                      createBaseVNode("strong", null, toDisplayString(processResult.value.failed_count), 1),
                      _cache[25] || (_cache[25] = createTextVNode(" failed"))
                    ]),
                    processResult.value.new_success_amount > 0 ? (openBlock(), createElementBlock("p", _hoisted_41, " Added NPR " + toDisplayString(formatAmount(processResult.value.new_success_amount)) + " to today's total ", 1)) : createCommentVNode("", true)
                  ], 64))
                ], 2)
              ]),
              createBaseVNode("button", {
                onClick: _cache[3] || (_cache[3] = ($event) => processResult.value = null),
                class: "flex-shrink-0 text-gray-500 hover:text-gray-700"
              }, _cache[26] || (_cache[26] = [
                createBaseVNode("svg", {
                  class: "w-5 h-5",
                  fill: "none",
                  stroke: "currentColor",
                  viewBox: "0 0 24 24"
                }, [
                  createBaseVNode("path", {
                    "stroke-linecap": "round",
                    "stroke-linejoin": "round",
                    "stroke-width": "2",
                    d: "M6 18L18 6M6 6l12 12"
                  })
                ], -1)
              ]))
            ])
          ], 2)) : createCommentVNode("", true),
          createBaseVNode("section", _hoisted_42, [
            loadingData.value ? (openBlock(), createElementBlock("div", _hoisted_43, _cache[27] || (_cache[27] = [
              createBaseVNode("div", { class: "animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto" }, null, -1),
              createBaseVNode("p", { class: "mt-4 text-gray-600" }, "Loading data...", -1)
            ]))) : !hasData.value ? (openBlock(), createElementBlock("div", _hoisted_44, _cache[28] || (_cache[28] = [
              createBaseVNode("svg", {
                class: "mx-auto h-12 w-12 text-gray-400",
                fill: "none",
                stroke: "currentColor",
                viewBox: "0 0 24 24"
              }, [
                createBaseVNode("path", {
                  "stroke-linecap": "round",
                  "stroke-linejoin": "round",
                  "stroke-width": "2",
                  d: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                })
              ], -1),
              createBaseVNode("p", { class: "mt-4 text-gray-600" }, "No data found for today.", -1)
            ]))) : selectedViewMode.value === "username" ? (openBlock(), createElementBlock("div", _hoisted_45, [
              _cache[29] || (_cache[29] = createBaseVNode("h3", { class: "text-lg font-semibold text-gray-900 mb-4" }, "Success Amount by Username", -1)),
              createBaseVNode("div", _hoisted_46, [
                (openBlock(true), createElementBlock(Fragment, null, renderList(usernameData.value, (item) => {
                  return openBlock(), createElementBlock("div", {
                    key: item.username,
                    class: normalizeClass([
                      "p-4 rounded-lg border-2 transition-all",
                      item.username === unref(session).user ? "bg-blue-50 border-blue-200 shadow-md" : "bg-gray-50 border-gray-200 hover:shadow-md"
                    ])
                  }, [
                    createBaseVNode("div", _hoisted_47, [
                      createBaseVNode("div", _hoisted_48, [
                        createBaseVNode("div", _hoisted_49, [
                          createBaseVNode("span", _hoisted_50, toDisplayString(item.full_name || item.username), 1),
                          item.username === unref(session).user ? (openBlock(), createElementBlock("span", _hoisted_51, " You ")) : createCommentVNode("", true)
                        ]),
                        createBaseVNode("div", _hoisted_52, toDisplayString(item.username), 1),
                        createBaseVNode("div", _hoisted_53, toDisplayString(item.count) + " payment" + toDisplayString(item.count !== 1 ? "s" : ""), 1)
                      ]),
                      createBaseVNode("div", _hoisted_54, [
                        createBaseVNode("div", _hoisted_55, "NPR " + toDisplayString(formatAmount(item.total_amount)), 1)
                      ])
                    ])
                  ], 2);
                }), 128))
              ])
            ])) : selectedViewMode.value === "customer" ? (openBlock(), createElementBlock("div", _hoisted_56, [
              _cache[30] || (_cache[30] = createBaseVNode("h3", { class: "text-lg font-semibold text-gray-900 mb-4" }, "Success Amount by Customer", -1)),
              createBaseVNode("div", _hoisted_57, [
                (openBlock(true), createElementBlock(Fragment, null, renderList(customerData.value, (item) => {
                  return openBlock(), createElementBlock("div", {
                    key: item.customer,
                    class: "p-4 rounded-lg bg-gray-50 border-2 border-gray-200 hover:shadow-md transition-all"
                  }, [
                    createBaseVNode("div", _hoisted_58, [
                      createBaseVNode("div", _hoisted_59, [
                        createBaseVNode("div", _hoisted_60, toDisplayString(item.customer_name), 1),
                        createBaseVNode("div", _hoisted_61, "Code: " + toDisplayString(item.customer), 1),
                        createBaseVNode("div", _hoisted_62, toDisplayString(item.count) + " payment" + toDisplayString(item.count !== 1 ? "s" : ""), 1)
                      ]),
                      createBaseVNode("div", _hoisted_63, [
                        createBaseVNode("div", _hoisted_64, "NPR " + toDisplayString(formatAmount(item.total_amount)), 1)
                      ])
                    ])
                  ]);
                }), 128))
              ])
            ])) : selectedViewMode.value === "transaction" ? (openBlock(), createElementBlock("div", _hoisted_65, [
              _cache[35] || (_cache[35] = createBaseVNode("h3", { class: "text-lg font-semibold text-gray-900 mb-4" }, "Transaction Details", -1)),
              createBaseVNode("div", _hoisted_66, [
                createBaseVNode("div", _hoisted_67, [
                  (openBlock(true), createElementBlock(Fragment, null, renderList(transactionData.value, (txn) => {
                    return openBlock(), createElementBlock("div", {
                      key: txn.name,
                      class: "p-4 rounded-lg bg-gray-50 border-2 border-gray-200 hover:shadow-md transition-all"
                    }, [
                      createBaseVNode("div", _hoisted_68, [
                        createBaseVNode("div", null, [
                          _cache[31] || (_cache[31] = createBaseVNode("div", { class: "text-xs text-gray-500 mb-1" }, "Amount", -1)),
                          createBaseVNode("div", _hoisted_69, "NPR " + toDisplayString(formatAmount(txn.amount)), 1)
                        ]),
                        createBaseVNode("div", null, [
                          _cache[32] || (_cache[32] = createBaseVNode("div", { class: "text-xs text-gray-500 mb-1" }, "Customer", -1)),
                          createBaseVNode("div", _hoisted_70, toDisplayString(txn.customer_name || txn.customer), 1),
                          createBaseVNode("div", _hoisted_71, toDisplayString(txn.customer), 1)
                        ]),
                        createBaseVNode("div", null, [
                          _cache[33] || (_cache[33] = createBaseVNode("div", { class: "text-xs text-gray-500 mb-1" }, "Created By", -1)),
                          createBaseVNode("div", _hoisted_72, toDisplayString(txn.owner_full_name || txn.owner), 1),
                          createBaseVNode("div", _hoisted_73, toDisplayString(txn.owner), 1)
                        ]),
                        createBaseVNode("div", null, [
                          _cache[34] || (_cache[34] = createBaseVNode("div", { class: "text-xs text-gray-500 mb-1" }, "Time", -1)),
                          createBaseVNode("div", _hoisted_74, toDisplayString(formatDateTime(txn.creation)), 1),
                          txn.payment_entry ? (openBlock(), createElementBlock("div", _hoisted_75, [
                            createBaseVNode("a", {
                              href: `/app/payment-entry/${txn.payment_entry}`,
                              target: "_blank",
                              class: "hover:underline"
                            }, " View Payment ", 8, _hoisted_76)
                          ])) : createCommentVNode("", true)
                        ])
                      ])
                    ]);
                  }), 128))
                ])
              ])
            ])) : createCommentVNode("", true)
          ])
        ])
      ]);
    };
  }
};
const PayDashboard = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-9fc4a308"]]);
export {
  PayDashboard as default
};
//# sourceMappingURL=PayDashboard-EcOW0ztI.js.map
