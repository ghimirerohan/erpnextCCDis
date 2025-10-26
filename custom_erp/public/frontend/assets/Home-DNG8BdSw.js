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
import { g as ref, s as reactive, c as computed, l as watch, k as onMounted, a as createElementBlock, b as createBaseVNode, t as toDisplayString, L as unref, z as createVNode, A as withCtx, n as normalizeClass, e as createCommentVNode, y as createBlock, B as withDirectives, ac as vModelText, F as Fragment, M as renderList, ad as createStaticVNode, aa as resolveComponent, o as openBlock, I as createTextVNode } from "./vendor-DNPaXrxF.js";
import { j as _export_sfc, c as createResource, k as _sfc_main$1 } from "./ui-C-4uyU25.js";
import { s as session } from "./index-DAX_0W7Y.js";
const _hoisted_1 = { class: "min-h-screen bg-gray-50" };
const _hoisted_2 = { class: "bg-white shadow-sm border-b border-gray-200" };
const _hoisted_3 = { class: "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8" };
const _hoisted_4 = { class: "flex justify-between items-center py-6" };
const _hoisted_5 = { class: "text-sm text-gray-600" };
const _hoisted_6 = { class: "flex gap-2" };
const _hoisted_7 = { class: "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8" };
const _hoisted_8 = { class: "bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8" };
const _hoisted_9 = { class: "grid grid-cols-1 md:grid-cols-3 gap-4" };
const _hoisted_10 = { class: "relative" };
const _hoisted_11 = { class: "relative" };
const _hoisted_12 = {
  key: 0,
  class: "border border-gray-300 rounded-md p-3"
};
const _hoisted_13 = { class: "text-sm font-medium text-gray-900" };
const _hoisted_14 = { class: "text-xs text-gray-600 mt-1" };
const _hoisted_15 = { key: 1 };
const _hoisted_16 = { class: "flex flex-wrap gap-2 mb-3" };
const _hoisted_17 = {
  key: 0,
  class: "p-3 border border-gray-200 rounded-md text-sm text-gray-700"
};
const _hoisted_18 = { key: 0 };
const _hoisted_19 = { key: 1 };
const _hoisted_20 = {
  key: 1,
  class: "p-3 border border-gray-200 rounded-md"
};
const _hoisted_21 = {
  key: 0,
  class: "mt-2 text-sm text-gray-600"
};
const _hoisted_22 = {
  key: 2,
  class: "p-3 border border-gray-200 rounded-md"
};
const _hoisted_23 = {
  key: 0,
  class: "mt-2 text-sm text-gray-500"
};
const _hoisted_24 = { class: "mt-4 flex justify-end" };
const _hoisted_25 = { class: "bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6" };
const _hoisted_26 = { class: "flex items-center justify-between" };
const _hoisted_27 = { class: "flex bg-gray-100 rounded-lg p-1" };
const _hoisted_28 = {
  key: 0,
  class: "flex justify-center items-center py-12"
};
const _hoisted_29 = {
  key: 2,
  class: "space-y-6"
};
const _hoisted_30 = { class: "bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden" };
const _hoisted_31 = { class: "px-6 py-4 border-b border-gray-200" };
const _hoisted_32 = { class: "text-lg font-semibold text-gray-900" };
const _hoisted_33 = { class: "overflow-x-auto" };
const _hoisted_34 = { class: "min-w-full divide-y divide-gray-200" };
const _hoisted_35 = { class: "bg-white divide-y divide-gray-200" };
const _hoisted_36 = { class: "px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600" };
const _hoisted_37 = { class: "px-6 py-4 whitespace-nowrap text-sm text-gray-900" };
const _hoisted_38 = { class: "px-6 py-4 whitespace-nowrap text-sm text-gray-900" };
const _hoisted_39 = { class: "px-6 py-4 whitespace-nowrap" };
const _hoisted_40 = { class: "px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 font-medium" };
const _hoisted_41 = { class: "px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900" };
const _hoisted_42 = { class: "px-6 py-4 border-b border-gray-200" };
const _hoisted_43 = { class: "text-md font-semibold text-gray-900" };
const _hoisted_44 = { class: "text-sm text-gray-600" };
const _hoisted_45 = { class: "overflow-x-auto" };
const _hoisted_46 = { class: "min-w-full divide-y divide-gray-200" };
const _hoisted_47 = { class: "bg-white divide-y divide-gray-200" };
const _hoisted_48 = { class: "px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900" };
const _hoisted_49 = { class: "px-6 py-4 text-sm text-gray-900" };
const _hoisted_50 = { class: "px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900" };
const _hoisted_51 = { class: "px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900" };
const _hoisted_52 = { class: "px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 font-medium" };
const _hoisted_53 = {
  key: 3,
  class: "space-y-6"
};
const _hoisted_54 = { class: "bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden" };
const _hoisted_55 = { class: "px-6 py-4 border-b border-gray-200" };
const _hoisted_56 = { class: "text-lg font-semibold text-gray-900" };
const _hoisted_57 = { class: "overflow-x-auto" };
const _hoisted_58 = { class: "min-w-full divide-y divide-gray-200" };
const _hoisted_59 = { class: "bg-white divide-y divide-gray-200" };
const _hoisted_60 = { class: "px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900" };
const _hoisted_61 = { class: "px-6 py-4 whitespace-nowrap text-sm text-gray-900" };
const _hoisted_62 = { class: "px-6 py-4 whitespace-nowrap text-sm text-center text-gray-900" };
const _hoisted_63 = { class: "px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 font-medium" };
const _hoisted_64 = { class: "px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900" };
const _hoisted_65 = { class: "px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900" };
const _hoisted_66 = { class: "px-6 py-4 border-b border-gray-200" };
const _hoisted_67 = { class: "text-md font-semibold text-gray-900" };
const _hoisted_68 = { class: "text-sm text-gray-600" };
const _hoisted_69 = { class: "overflow-x-auto" };
const _hoisted_70 = { class: "min-w-full divide-y divide-gray-200" };
const _hoisted_71 = { class: "bg-white divide-y divide-gray-200" };
const _hoisted_72 = { class: "px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900" };
const _hoisted_73 = { class: "px-6 py-4 text-sm text-gray-900" };
const _hoisted_74 = { class: "px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900" };
const _hoisted_75 = { class: "px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900" };
const _hoisted_76 = { class: "px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900 font-medium" };
const _hoisted_77 = {
  key: 4,
  class: "text-center py-12"
};
const _sfc_main = {
  __name: "Home",
  setup(__props) {
    const loading = ref(false);
    const error = ref("");
    const viewMode = ref("bill");
    const data = ref([]);
    const summaryData = ref([]);
    const filters = reactive({
      customer: "",
      from_date: "",
      to_date: ""
    });
    const selectionLocked = ref(false);
    const selectMode = ref("list");
    const extractLoading = ref(false);
    const extractError = ref("");
    const selectedCustomer = ref({ customer: "", customer_name: "", customer_code: "", invoice_no: "" });
    const qrSupported = typeof window !== "undefined" && "BarcodeDetector" in window;
    const qrVideo = ref(null);
    const selectedCustomerLabel = ref("");
    const customerListLoading = ref(false);
    const customerList = ref([]);
    const customerOptions = computed(() => {
      return customerList.value.map((c) => ({
        label: c.customer_name || c.name,
        value: c.name,
        description: c.name
      }));
    });
    const salesInvoicesResource = createResource({
      url: "custom_erp.custom_erp.sales_invoice.api.get_sales_invoices",
      auto: false,
      onSuccess: (result) => {
        if (result.success) {
          data.value = result.data;
          error.value = "";
        } else {
          error.value = result.error || "Failed to load sales invoices";
        }
      },
      onError: (err) => {
        error.value = "Failed to load sales invoices: " + err.message;
      }
    });
    const salesInvoiceSummaryResource = createResource({
      url: "custom_erp.custom_erp.sales_invoice.api.get_sales_invoice_summary",
      auto: false,
      onSuccess: (result) => {
        if (result.success) {
          summaryData.value = result.data;
          error.value = "";
        } else {
          error.value = result.error || "Failed to load summary data";
        }
      },
      onError: (err) => {
        error.value = "Failed to load summary data: " + err.message;
      }
    });
    const loadData = () => __async(this, null, function* () {
      if (!filters.customer || !filters.from_date || !filters.to_date) {
        error.value = "Please fill in all required fields";
        return;
      }
      loading.value = true;
      error.value = "";
      try {
        const filtersParam = JSON.stringify(filters);
        if (viewMode.value === "bill") {
          yield salesInvoicesResource.fetch({ filters: filtersParam });
        } else {
          yield salesInvoiceSummaryResource.fetch({ filters: filtersParam });
        }
      } catch (err) {
        error.value = "Failed to load data: " + err.message;
      } finally {
        loading.value = false;
      }
    });
    const formatDate = (dateString) => {
      if (!dateString) return "";
      const date = new Date(dateString);
      return date.toLocaleDateString();
    };
    const formatCurrency = (amount) => {
      if (amount === null || amount === void 0) return "0.00";
      return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD"
      }).format(amount);
    };
    const getStatusTheme = (status) => {
      const themes = {
        "Paid": "green",
        "Unpaid": "red",
        "Overdue": "orange",
        "Draft": "gray",
        "Submitted": "blue"
      };
      return themes[status] || "gray";
    };
    const resetSelection = () => {
      selectionLocked.value = false;
      filters.customer = "";
      selectedCustomer.value = { customer: "", customer_name: "", customer_code: "", invoice_no: "" };
      selectedCustomerLabel.value = "";
      extractError.value = "";
      customerList.value = [];
    };
    const onPhotoSelected = (event) => __async(this, null, function* () {
      var _a, _b;
      const file = (_b = (_a = event == null ? void 0 : event.target) == null ? void 0 : _a.files) == null ? void 0 : _b[0];
      if (!file) return;
      extractError.value = "";
      extractLoading.value = true;
      try {
        const b64 = yield new Promise((resolve, reject) => {
          const reader = new FileReader();
          reader.onload = () => resolve(String(reader.result));
          reader.onerror = reject;
          reader.readAsDataURL(file);
        });
        const res = yield fetch("/api/method/custom_erp.custom_erp.purchase_invoice.api.extract_invoice", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ image_data: b64 })
        });
        const json = yield res.json();
        const msg = (json == null ? void 0 : json.message) || json;
        if (!res.ok || !(msg == null ? void 0 : msg.success) || !(msg == null ? void 0 : msg.data)) {
          throw new Error((msg == null ? void 0 : msg.error) || `Extraction failed (${res.status})`);
        }
        const invoiceBillNumber = msg.data.invoiceNumber || "";
        const customerName = msg.data.customerName || "";
        const resolved = yield resolveCustomer({ invoiceBillNumber, customerCode: "" });
        if (!resolved) {
          throw new Error("Could not find matching customer from code or invoice");
        }
        filters.customer = resolved.customer;
        selectedCustomer.value = {
          customer: resolved.customer,
          customer_name: resolved.customer_name || customerName || resolved.customer,
          customer_code: "",
          invoice_no: invoiceBillNumber || ""
        };
        selectionLocked.value = true;
      } catch (e) {
        extractError.value = e.message || "Failed to process image";
      } finally {
        extractLoading.value = false;
      }
    });
    function resolveCustomer(_0) {
      return __async(this, arguments, function* ({ invoiceBillNumber, customerCode }) {
        if (customerCode) {
          const fieldsToTry = ["mobile_no", "customer_code"];
          for (const field of fieldsToTry) {
            try {
              const byCode = yield findCustomerByField(field, customerCode);
              if (byCode) return byCode;
            } catch (_) {
            }
          }
        }
        if (invoiceBillNumber) {
          try {
            const invRes = yield fetch(`/api/resource/Sales%20Invoice/${encodeURIComponent(invoiceBillNumber)}`);
            if (invRes.ok) {
              const invJson = yield invRes.json();
              const doc = invJson == null ? void 0 : invJson.data;
              if (doc == null ? void 0 : doc.customer) {
                return { customer: doc.customer, customer_name: doc.customer_name || doc.customer };
              }
            }
          } catch (_) {
          }
        }
        return null;
      });
    }
    function findCustomerByField(field, value) {
      return __async(this, null, function* () {
        const params = new URLSearchParams();
        params.set("fields", JSON.stringify(["name", "customer_name"]));
        params.set("filters", JSON.stringify([[field, "=", String(value)]]));
        params.set("limit_page_length", "1");
        const res = yield fetch(`/api/resource/Customer?${params.toString()}`);
        if (!res.ok) return null;
        const json = yield res.json();
        const list = json == null ? void 0 : json.data;
        if (Array.isArray(list) && list.length > 0) {
          return { customer: list[0].name, customer_name: list[0].customer_name || list[0].name };
        }
        return null;
      });
    }
    const handleCustomerQuery = (query) => __async(this, null, function* () {
      if (!query || query.length < 2) {
        customerList.value = [];
        return;
      }
      customerListLoading.value = true;
      try {
        const params = new URLSearchParams();
        params.set("fields", JSON.stringify(["name", "customer_name", "customer_code", "mobile_no"]));
        params.set("filters", JSON.stringify([]));
        params.set("or_filters", JSON.stringify([
          ["customer_name", "like", `%${query}%`],
          ["name", "like", `%${query}%`],
          ["customer_code", "like", `%${query}%`],
          ["mobile_no", "like", `%${query}%`]
        ]));
        params.set("limit_page_length", "20");
        const res = yield fetch(`/api/resource/Customer?${params.toString()}`);
        if (res.ok) {
          const json = yield res.json();
          customerList.value = (json == null ? void 0 : json.data) || [];
        }
      } catch (e) {
        console.error("Failed to fetch customers:", e);
        customerList.value = [];
      } finally {
        customerListLoading.value = false;
      }
    });
    const onCustomerSelected = (option) => __async(this, null, function* () {
      if (!option || !option.value) return;
      try {
        const res = yield fetch(`/api/resource/Customer/${encodeURIComponent(option.value)}`);
        if (!res.ok) throw new Error("Failed to fetch customer details");
        const json = yield res.json();
        const customer = json == null ? void 0 : json.data;
        if (customer) {
          filters.customer = customer.name;
          selectedCustomer.value = {
            customer: customer.name,
            customer_name: customer.customer_name || customer.name,
            customer_code: customer.customer_code || customer.mobile_no || "",
            invoice_no: ""
          };
          selectedCustomerLabel.value = customer.customer_name || customer.name;
          selectionLocked.value = true;
        }
      } catch (e) {
        error.value = "Failed to load customer details: " + (e.message || "Unknown error");
      }
    });
    watch(viewMode, () => {
      if (filters.customer && filters.from_date && filters.to_date) {
        loadData();
      }
    });
    onMounted(() => {
      const today = /* @__PURE__ */ new Date();
      const thirtyDaysAgo = new Date(today.getTime() - 30 * 24 * 60 * 60 * 1e3);
      filters.to_date = today.toISOString().split("T")[0];
      filters.from_date = thirtyDaysAgo.toISOString().split("T")[0];
    });
    return (_ctx, _cache) => {
      const _component_Button = resolveComponent("Button");
      const _component_Alert = resolveComponent("Alert");
      const _component_Badge = resolveComponent("Badge");
      return openBlock(), createElementBlock("div", _hoisted_1, [
        createBaseVNode("div", _hoisted_2, [
          createBaseVNode("div", _hoisted_3, [
            createBaseVNode("div", _hoisted_4, [
              createBaseVNode("div", null, [
                _cache[10] || (_cache[10] = createBaseVNode("h1", { class: "text-2xl font-bold text-gray-900" }, "Sales Invoice Dashboard", -1)),
                createBaseVNode("p", _hoisted_5, "Welcome " + toDisplayString(unref(session).user) + "!", 1)
              ]),
              createBaseVNode("div", _hoisted_6, [
                createVNode(_component_Button, {
                  onClick: _cache[0] || (_cache[0] = ($event) => _ctx.$router.push({ name: "Scanner" })),
                  theme: "blue",
                  variant: "solid"
                }, {
                  default: withCtx(() => _cache[11] || (_cache[11] = [
                    createTextVNode(" Open Scanner ")
                  ])),
                  _: 1,
                  __: [11]
                }),
                createVNode(_component_Button, {
                  onClick: _cache[1] || (_cache[1] = ($event) => unref(session).logout.submit()),
                  theme: "gray",
                  variant: "outline"
                }, {
                  default: withCtx(() => _cache[12] || (_cache[12] = [
                    createTextVNode(" Logout ")
                  ])),
                  _: 1,
                  __: [12]
                })
              ])
            ])
          ])
        ]),
        createBaseVNode("div", _hoisted_7, [
          createBaseVNode("div", _hoisted_8, [
            _cache[20] || (_cache[20] = createBaseVNode("h2", { class: "text-lg font-semibold text-gray-900 mb-4" }, "Filters", -1)),
            createBaseVNode("div", _hoisted_9, [
              createBaseVNode("div", _hoisted_10, [
                _cache[16] || (_cache[16] = createBaseVNode("label", { class: "block text-sm font-medium text-gray-700 mb-2" }, "Customer", -1)),
                createBaseVNode("div", _hoisted_11, [
                  selectionLocked.value ? (openBlock(), createElementBlock("div", _hoisted_12, [
                    createBaseVNode("div", _hoisted_13, toDisplayString(selectedCustomer.value.customer_name), 1),
                    createBaseVNode("div", _hoisted_14, [
                      createBaseVNode("span", null, "Code: " + toDisplayString(selectedCustomer.value.customer_code || "—"), 1),
                      _cache[13] || (_cache[13] = createBaseVNode("span", { class: "mx-2" }, "|", -1)),
                      createBaseVNode("span", null, "Invoice: " + toDisplayString(selectedCustomer.value.invoice_no || "—"), 1)
                    ]),
                    createBaseVNode("div", { class: "mt-2" }, [
                      createBaseVNode("button", {
                        onClick: resetSelection,
                        class: "text-sm text-blue-600 underline"
                      }, "Change selection")
                    ])
                  ])) : (openBlock(), createElementBlock("div", _hoisted_15, [
                    createBaseVNode("div", _hoisted_16, [
                      createBaseVNode("button", {
                        onClick: _cache[2] || (_cache[2] = ($event) => selectMode.value = "list"),
                        class: normalizeClass([
                          "flex-1 min-w-[120px] px-3 py-2 text-sm font-medium rounded-md border transition-colors",
                          selectMode.value === "list" ? "bg-blue-50 border-blue-400 text-blue-700" : "bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
                        ])
                      }, " Customer List ", 2),
                      createBaseVNode("button", {
                        onClick: _cache[3] || (_cache[3] = ($event) => selectMode.value = "qr"),
                        class: normalizeClass([
                          "flex-1 min-w-[120px] px-3 py-2 text-sm font-medium rounded-md border transition-colors",
                          selectMode.value === "qr" ? "bg-blue-50 border-blue-400 text-blue-700" : "bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
                        ])
                      }, " QR Scanner ", 2),
                      createBaseVNode("button", {
                        onClick: _cache[4] || (_cache[4] = ($event) => selectMode.value = "photo"),
                        class: normalizeClass([
                          "flex-1 min-w-[120px] px-3 py-2 text-sm font-medium rounded-md border transition-colors",
                          selectMode.value === "photo" ? "bg-blue-50 border-blue-400 text-blue-700" : "bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
                        ])
                      }, " Photo / Camera ", 2)
                    ]),
                    selectMode.value === "qr" ? (openBlock(), createElementBlock("div", _hoisted_17, [
                      unref(qrSupported) ? (openBlock(), createElementBlock("div", _hoisted_18, [
                        _cache[14] || (_cache[14] = createBaseVNode("div", { class: "mb-2" }, "Point your camera at the QR code.", -1)),
                        createBaseVNode("video", {
                          ref_key: "qrVideo",
                          ref: qrVideo,
                          class: "w-full rounded",
                          autoplay: "",
                          playsinline: "",
                          muted: ""
                        }, null, 512),
                        _cache[15] || (_cache[15] = createBaseVNode("div", { class: "mt-2 text-xs text-gray-500" }, "Scanning...", -1))
                      ])) : (openBlock(), createElementBlock("div", _hoisted_19, " QR scanning is not supported on this device/browser. Please use Photo. "))
                    ])) : selectMode.value === "photo" ? (openBlock(), createElementBlock("div", _hoisted_20, [
                      createBaseVNode("input", {
                        type: "file",
                        accept: "image/*",
                        capture: "environment",
                        onChange: onPhotoSelected
                      }, null, 32),
                      extractLoading.value ? (openBlock(), createElementBlock("div", _hoisted_21, "Processing image...")) : createCommentVNode("", true),
                      extractError.value ? (openBlock(), createBlock(_component_Alert, {
                        key: 1,
                        theme: "red",
                        class: "mt-2"
                      }, {
                        default: withCtx(() => [
                          createTextVNode(toDisplayString(extractError.value), 1)
                        ]),
                        _: 1
                      })) : createCommentVNode("", true)
                    ])) : selectMode.value === "list" ? (openBlock(), createElementBlock("div", _hoisted_22, [
                      createVNode(unref(_sfc_main$1), {
                        modelValue: selectedCustomerLabel.value,
                        "onUpdate:modelValue": _cache[5] || (_cache[5] = ($event) => selectedCustomerLabel.value = $event),
                        options: customerOptions.value,
                        loading: customerListLoading.value,
                        debounce: 300,
                        placeholder: "Search by customer name or code...",
                        "onUpdate:query": handleCustomerQuery,
                        onSelect: onCustomerSelected,
                        clearable: true
                      }, null, 8, ["modelValue", "options", "loading"]),
                      !filters.customer ? (openBlock(), createElementBlock("p", _hoisted_23, "Start typing to search for a customer")) : createCommentVNode("", true)
                    ])) : createCommentVNode("", true)
                  ]))
                ])
              ]),
              createBaseVNode("div", null, [
                _cache[17] || (_cache[17] = createBaseVNode("label", { class: "block text-sm font-medium text-gray-700 mb-2" }, "From Date", -1)),
                withDirectives(createBaseVNode("input", {
                  type: "date",
                  "onUpdate:modelValue": _cache[6] || (_cache[6] = ($event) => filters.from_date = $event),
                  class: "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                  required: ""
                }, null, 512), [
                  [vModelText, filters.from_date]
                ])
              ]),
              createBaseVNode("div", null, [
                _cache[18] || (_cache[18] = createBaseVNode("label", { class: "block text-sm font-medium text-gray-700 mb-2" }, "To Date", -1)),
                withDirectives(createBaseVNode("input", {
                  type: "date",
                  "onUpdate:modelValue": _cache[7] || (_cache[7] = ($event) => filters.to_date = $event),
                  class: "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                  required: ""
                }, null, 512), [
                  [vModelText, filters.to_date]
                ])
              ])
            ]),
            createBaseVNode("div", _hoisted_24, [
              createVNode(_component_Button, {
                onClick: loadData,
                loading: loading.value,
                theme: "blue",
                variant: "solid",
                disabled: !filters.customer || !filters.from_date || !filters.to_date
              }, {
                default: withCtx(() => _cache[19] || (_cache[19] = [
                  createTextVNode(" Load Data ")
                ])),
                _: 1,
                __: [19]
              }, 8, ["loading", "disabled"])
            ])
          ]),
          createBaseVNode("div", _hoisted_25, [
            createBaseVNode("div", _hoisted_26, [
              _cache[21] || (_cache[21] = createBaseVNode("h2", { class: "text-lg font-semibold text-gray-900" }, "View Options", -1)),
              createBaseVNode("div", _hoisted_27, [
                createBaseVNode("button", {
                  onClick: _cache[8] || (_cache[8] = ($event) => viewMode.value = "bill"),
                  class: normalizeClass([
                    "px-4 py-2 text-sm font-medium rounded-md transition-colors",
                    viewMode.value === "bill" ? "bg-white text-blue-600 shadow-sm" : "text-gray-600 hover:text-gray-900"
                  ])
                }, " Bill-wise View ", 2),
                createBaseVNode("button", {
                  onClick: _cache[9] || (_cache[9] = ($event) => viewMode.value = "summary"),
                  class: normalizeClass([
                    "px-4 py-2 text-sm font-medium rounded-md transition-colors",
                    viewMode.value === "summary" ? "bg-white text-blue-600 shadow-sm" : "text-gray-600 hover:text-gray-900"
                  ])
                }, " Summary View ", 2)
              ])
            ])
          ]),
          loading.value ? (openBlock(), createElementBlock("div", _hoisted_28, _cache[22] || (_cache[22] = [
            createBaseVNode("div", { class: "animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" }, null, -1),
            createBaseVNode("span", { class: "ml-3 text-gray-600" }, "Loading data...", -1)
          ]))) : createCommentVNode("", true),
          error.value ? (openBlock(), createBlock(_component_Alert, {
            key: 1,
            theme: "red",
            class: "mb-6"
          }, {
            default: withCtx(() => [
              createTextVNode(toDisplayString(error.value), 1)
            ]),
            _: 1
          })) : createCommentVNode("", true),
          viewMode.value === "bill" && !loading.value && data.value.length > 0 ? (openBlock(), createElementBlock("div", _hoisted_29, [
            createBaseVNode("div", _hoisted_30, [
              createBaseVNode("div", _hoisted_31, [
                createBaseVNode("h3", _hoisted_32, " Sales Invoices (" + toDisplayString(data.value.length) + " invoices) ", 1)
              ]),
              createBaseVNode("div", _hoisted_33, [
                createBaseVNode("table", _hoisted_34, [
                  _cache[23] || (_cache[23] = createBaseVNode("thead", { class: "bg-gray-50" }, [
                    createBaseVNode("tr", null, [
                      createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Invoice "),
                      createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Date "),
                      createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Customer "),
                      createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Status "),
                      createBaseVNode("th", { class: "px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Total Amount "),
                      createBaseVNode("th", { class: "px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Outstanding ")
                    ])
                  ], -1)),
                  createBaseVNode("tbody", _hoisted_35, [
                    (openBlock(true), createElementBlock(Fragment, null, renderList(data.value, (invoice) => {
                      return openBlock(), createElementBlock("tr", {
                        key: invoice.name,
                        class: "hover:bg-gray-50"
                      }, [
                        createBaseVNode("td", _hoisted_36, toDisplayString(invoice.name), 1),
                        createBaseVNode("td", _hoisted_37, toDisplayString(formatDate(invoice.posting_date)), 1),
                        createBaseVNode("td", _hoisted_38, toDisplayString(invoice.customer_name), 1),
                        createBaseVNode("td", _hoisted_39, [
                          createVNode(_component_Badge, {
                            theme: getStatusTheme(invoice.status)
                          }, {
                            default: withCtx(() => [
                              createTextVNode(toDisplayString(invoice.status), 1)
                            ]),
                            _: 2
                          }, 1032, ["theme"])
                        ]),
                        createBaseVNode("td", _hoisted_40, toDisplayString(formatCurrency(invoice.grand_total)), 1),
                        createBaseVNode("td", _hoisted_41, toDisplayString(formatCurrency(invoice.outstanding_amount)), 1)
                      ]);
                    }), 128))
                  ])
                ])
              ])
            ]),
            (openBlock(true), createElementBlock(Fragment, null, renderList(data.value, (invoice) => {
              return openBlock(), createElementBlock("div", {
                key: `details-${invoice.name}`,
                class: "bg-white rounded-lg shadow-sm border border-gray-200"
              }, [
                createBaseVNode("div", _hoisted_42, [
                  createBaseVNode("h4", _hoisted_43, " Invoice: " + toDisplayString(invoice.name) + " - " + toDisplayString(invoice.customer_name), 1),
                  createBaseVNode("p", _hoisted_44, " Date: " + toDisplayString(formatDate(invoice.posting_date)) + " | Total: " + toDisplayString(formatCurrency(invoice.grand_total)), 1)
                ]),
                createBaseVNode("div", _hoisted_45, [
                  createBaseVNode("table", _hoisted_46, [
                    _cache[24] || (_cache[24] = createBaseVNode("thead", { class: "bg-gray-50" }, [
                      createBaseVNode("tr", null, [
                        createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Item "),
                        createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Description "),
                        createBaseVNode("th", { class: "px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Qty "),
                        createBaseVNode("th", { class: "px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Rate "),
                        createBaseVNode("th", { class: "px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Amount ")
                      ])
                    ], -1)),
                    createBaseVNode("tbody", _hoisted_47, [
                      (openBlock(true), createElementBlock(Fragment, null, renderList(invoice.items, (item) => {
                        return openBlock(), createElementBlock("tr", {
                          key: item.item_code,
                          class: "hover:bg-gray-50"
                        }, [
                          createBaseVNode("td", _hoisted_48, toDisplayString(item.item_code), 1),
                          createBaseVNode("td", _hoisted_49, toDisplayString(item.item_name), 1),
                          createBaseVNode("td", _hoisted_50, toDisplayString(item.qty) + " " + toDisplayString(item.uom), 1),
                          createBaseVNode("td", _hoisted_51, toDisplayString(formatCurrency(item.rate)), 1),
                          createBaseVNode("td", _hoisted_52, toDisplayString(formatCurrency(item.amount)), 1)
                        ]);
                      }), 128))
                    ])
                  ])
                ])
              ]);
            }), 128))
          ])) : createCommentVNode("", true),
          viewMode.value === "summary" && !loading.value && summaryData.value.length > 0 ? (openBlock(), createElementBlock("div", _hoisted_53, [
            createBaseVNode("div", _hoisted_54, [
              createBaseVNode("div", _hoisted_55, [
                createBaseVNode("h3", _hoisted_56, " Summary by Customer & Date (" + toDisplayString(summaryData.value.length) + " groups) ", 1)
              ]),
              createBaseVNode("div", _hoisted_57, [
                createBaseVNode("table", _hoisted_58, [
                  _cache[25] || (_cache[25] = createBaseVNode("thead", { class: "bg-gray-50" }, [
                    createBaseVNode("tr", null, [
                      createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Customer "),
                      createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Date "),
                      createBaseVNode("th", { class: "px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Invoices "),
                      createBaseVNode("th", { class: "px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Total Amount "),
                      createBaseVNode("th", { class: "px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Net Total "),
                      createBaseVNode("th", { class: "px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Outstanding ")
                    ])
                  ], -1)),
                  createBaseVNode("tbody", _hoisted_59, [
                    (openBlock(true), createElementBlock(Fragment, null, renderList(summaryData.value, (group) => {
                      return openBlock(), createElementBlock("tr", {
                        key: `${group.customer}-${group.posting_date}`,
                        class: "hover:bg-gray-50"
                      }, [
                        createBaseVNode("td", _hoisted_60, toDisplayString(group.customer_name), 1),
                        createBaseVNode("td", _hoisted_61, toDisplayString(formatDate(group.posting_date)), 1),
                        createBaseVNode("td", _hoisted_62, toDisplayString(group.invoice_count), 1),
                        createBaseVNode("td", _hoisted_63, toDisplayString(formatCurrency(group.total_amount)), 1),
                        createBaseVNode("td", _hoisted_64, toDisplayString(formatCurrency(group.net_total)), 1),
                        createBaseVNode("td", _hoisted_65, toDisplayString(formatCurrency(group.outstanding_amount)), 1)
                      ]);
                    }), 128))
                  ])
                ])
              ])
            ]),
            (openBlock(true), createElementBlock(Fragment, null, renderList(summaryData.value, (group) => {
              return openBlock(), createElementBlock("div", {
                key: `summary-${group.customer}-${group.posting_date}`,
                class: "bg-white rounded-lg shadow-sm border border-gray-200"
              }, [
                createBaseVNode("div", _hoisted_66, [
                  createBaseVNode("h4", _hoisted_67, toDisplayString(group.customer_name) + " - " + toDisplayString(formatDate(group.posting_date)), 1),
                  createBaseVNode("p", _hoisted_68, toDisplayString(group.invoice_count) + " invoices | Total: " + toDisplayString(formatCurrency(group.total_amount)), 1)
                ]),
                createBaseVNode("div", _hoisted_69, [
                  createBaseVNode("table", _hoisted_70, [
                    _cache[26] || (_cache[26] = createBaseVNode("thead", { class: "bg-gray-50" }, [
                      createBaseVNode("tr", null, [
                        createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Item "),
                        createBaseVNode("th", { class: "px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Description "),
                        createBaseVNode("th", { class: "px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Total Qty "),
                        createBaseVNode("th", { class: "px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Avg Rate "),
                        createBaseVNode("th", { class: "px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider" }, " Total Amount ")
                      ])
                    ], -1)),
                    createBaseVNode("tbody", _hoisted_71, [
                      (openBlock(true), createElementBlock(Fragment, null, renderList(group.items, (item) => {
                        return openBlock(), createElementBlock("tr", {
                          key: item.item_code,
                          class: "hover:bg-gray-50"
                        }, [
                          createBaseVNode("td", _hoisted_72, toDisplayString(item.item_code), 1),
                          createBaseVNode("td", _hoisted_73, toDisplayString(item.item_name), 1),
                          createBaseVNode("td", _hoisted_74, toDisplayString(item.total_qty) + " " + toDisplayString(item.uom), 1),
                          createBaseVNode("td", _hoisted_75, toDisplayString(formatCurrency(item.avg_rate)), 1),
                          createBaseVNode("td", _hoisted_76, toDisplayString(formatCurrency(item.total_amount)), 1)
                        ]);
                      }), 128))
                    ])
                  ])
                ])
              ]);
            }), 128))
          ])) : createCommentVNode("", true),
          !loading.value && data.value.length === 0 && summaryData.value.length === 0 ? (openBlock(), createElementBlock("div", _hoisted_77, _cache[27] || (_cache[27] = [
            createStaticVNode('<div class="text-gray-400 mb-4" data-v-48744dde><svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor" data-v-48744dde><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" data-v-48744dde></path></svg></div><h3 class="text-lg font-medium text-gray-900 mb-2" data-v-48744dde>No data found</h3><p class="text-gray-600" data-v-48744dde>Try adjusting your filters or selecting a different date range.</p>', 3)
          ]))) : createCommentVNode("", true)
        ])
      ]);
    };
  }
};
const Home = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-48744dde"]]);
export {
  Home as default
};
//# sourceMappingURL=Home-DNG8BdSw.js.map
