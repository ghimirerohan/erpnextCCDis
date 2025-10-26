var __defProp = Object.defineProperty;
var __defProps = Object.defineProperties;
var __getOwnPropDescs = Object.getOwnPropertyDescriptors;
var __getOwnPropSymbols = Object.getOwnPropertySymbols;
var __hasOwnProp = Object.prototype.hasOwnProperty;
var __propIsEnum = Object.prototype.propertyIsEnumerable;
var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
var __spreadValues = (a, b) => {
  for (var prop in b || (b = {}))
    if (__hasOwnProp.call(b, prop))
      __defNormalProp(a, prop, b[prop]);
  if (__getOwnPropSymbols)
    for (var prop of __getOwnPropSymbols(b)) {
      if (__propIsEnum.call(b, prop))
        __defNormalProp(a, prop, b[prop]);
    }
  return a;
};
var __spreadProps = (a, b) => __defProps(a, __getOwnPropDescs(b));
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
import { g as ref, s as reactive, c as computed, l as watch, k as onMounted, a as createElementBlock, b as createBaseVNode, t as toDisplayString, L as unref, z as createVNode, A as withCtx, B as withDirectives, aj as vModelRadio, I as createTextVNode, ac as vModelText, n as normalizeClass, N as withModifiers, e as createCommentVNode, y as createBlock, ak as vModelCheckbox, ad as createStaticVNode, F as Fragment, M as renderList, aa as resolveComponent, o as openBlock, al as vModelSelect } from "./vendor-DNPaXrxF.js";
import { j as _export_sfc } from "./ui-C-4uyU25.js";
import { s as session } from "./index-DA5oEbtt.js";
const _hoisted_1 = { class: "min-h-screen bg-gray-50" };
const _hoisted_2 = { class: "bg-white shadow-sm border-b border-gray-200 sticky top-0 z-20" };
const _hoisted_3 = { class: "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8" };
const _hoisted_4 = { class: "flex justify-between items-center py-6" };
const _hoisted_5 = { class: "text-sm text-gray-600" };
const _hoisted_6 = { class: "max-w-7xl mx-auto px-3 sm:px-4 lg:px-6 py-4 sm:py-8" };
const _hoisted_7 = { class: "bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8" };
const _hoisted_8 = { class: "mb-4" };
const _hoisted_9 = { class: "flex gap-4" };
const _hoisted_10 = { class: "flex items-center gap-2" };
const _hoisted_11 = { class: "flex items-center gap-2" };
const _hoisted_12 = { class: "grid grid-cols-1 md:grid-cols-2 gap-4 mb-4" };
const _hoisted_13 = {
  key: 0,
  class: "mb-4"
};
const _hoisted_14 = ["src"];
const _hoisted_15 = {
  key: 1,
  class: "space-y-4"
};
const _hoisted_16 = { class: "flex flex-col sm:flex-row gap-3 justify-center" };
const _hoisted_17 = { class: "flex-1 cursor-pointer" };
const _hoisted_18 = ["disabled"];
const _hoisted_19 = { key: 0 };
const _hoisted_20 = { key: 1 };
const _hoisted_21 = { class: "mt-6 flex gap-3" };
const _hoisted_22 = {
  key: 0,
  class: "bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8"
};
const _hoisted_23 = { class: "flex items-center" };
const _hoisted_24 = {
  key: 0,
  class: "flex-shrink-0 w-5 h-5 text-orange-400"
};
const _hoisted_25 = {
  key: 1,
  class: "flex-shrink-0 w-5 h-5 text-blue-400"
};
const _hoisted_26 = { class: "ml-3" };
const _hoisted_27 = { class: "text-xs mt-1 text-gray-600" };
const _hoisted_28 = { class: "grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4" };
const _hoisted_29 = { class: "mt-4 grid md:grid-cols-3 gap-3 sm:gap-4" };
const _hoisted_30 = { class: "flex items-center mt-2" };
const _hoisted_31 = { class: "text-xs text-gray-500 mt-1" };
const _hoisted_32 = {
  key: 0,
  class: "text-xs text-orange-600 mt-1"
};
const _hoisted_33 = { class: "md:col-span-2" };
const _hoisted_34 = {
  key: 0,
  class: "mb-4"
};
const _hoisted_35 = ["src"];
const _hoisted_36 = {
  key: 1,
  class: "space-y-4"
};
const _hoisted_37 = { class: "flex flex-col sm:flex-row gap-3 justify-center" };
const _hoisted_38 = { class: "flex-1 cursor-pointer" };
const _hoisted_39 = ["disabled"];
const _hoisted_40 = { key: 0 };
const _hoisted_41 = { key: 1 };
const _hoisted_42 = { class: "md:col-span-3" };
const _hoisted_43 = {
  key: 1,
  class: "mt-6"
};
const _hoisted_44 = { class: "flex justify-between items-center mb-4" };
const _hoisted_45 = {
  key: 0,
  class: "flex items-center gap-2"
};
const _hoisted_46 = { class: "flex items-center justify-between" };
const _hoisted_47 = { class: "flex items-center" };
const _hoisted_48 = {
  key: 0,
  class: "flex-shrink-0 w-5 h-5 text-green-400"
};
const _hoisted_49 = {
  key: 1,
  class: "flex-shrink-0 w-5 h-5 text-yellow-400"
};
const _hoisted_50 = { class: "ml-3" };
const _hoisted_51 = {
  key: 0,
  class: "text-sm text-yellow-700 mt-1"
};
const _hoisted_52 = { class: "flex space-x-2" };
const _hoisted_53 = {
  key: 1,
  class: "mb-4 p-3 rounded-md bg-gray-50 border border-gray-200"
};
const _hoisted_54 = { class: "flex items-center justify-between" };
const _hoisted_55 = { class: "overflow-x-auto border border-gray-200 rounded-lg" };
const _hoisted_56 = { class: "min-w-full divide-y divide-gray-200" };
const _hoisted_57 = { class: "bg-white divide-y divide-gray-200" };
const _hoisted_58 = { class: "px-2 sm:px-3 py-3 text-sm" };
const _hoisted_59 = { class: "flex items-center space-x-2" };
const _hoisted_60 = ["onUpdate:modelValue"];
const _hoisted_61 = ["onClick"];
const _hoisted_62 = {
  key: 1,
  class: "flex-shrink-0 w-8 h-8 bg-green-500 text-white rounded-full flex items-center justify-center text-sm"
};
const _hoisted_63 = { class: "px-2 sm:px-3 py-3 text-sm" };
const _hoisted_64 = ["onUpdate:modelValue"];
const _hoisted_65 = { class: "px-2 sm:px-3 py-3 text-sm text-center" };
const _hoisted_66 = ["onUpdate:modelValue"];
const _hoisted_67 = { class: "px-2 sm:px-3 py-3 text-sm text-center" };
const _hoisted_68 = ["onUpdate:modelValue"];
const _hoisted_69 = { class: "px-2 sm:px-3 py-3 text-sm text-center" };
const _hoisted_70 = ["onUpdate:modelValue"];
const _hoisted_71 = { class: "px-2 sm:px-3 py-3 text-center" };
const _hoisted_72 = ["onUpdate:modelValue"];
const _hoisted_73 = { class: "px-2 sm:px-3 py-3 text-sm text-center" };
const _hoisted_74 = { class: "mt-6 flex justify-end" };
const _hoisted_75 = {
  key: 0,
  class: "fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
};
const _hoisted_76 = { class: "bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto" };
const _hoisted_77 = { class: "px-6 py-4 space-y-4" };
const _hoisted_78 = { class: "px-6 py-4 border-t border-gray-200 flex justify-end space-x-3" };
const _hoisted_79 = {
  key: 1,
  class: "fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
};
const _hoisted_80 = { class: "bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto" };
const _hoisted_81 = { class: "px-6 py-4 border-b border-gray-200" };
const _hoisted_82 = { class: "text-lg font-medium text-gray-900" };
const _hoisted_83 = { class: "px-6 py-4" };
const _hoisted_84 = {
  key: 0,
  class: "flex justify-center items-center py-8"
};
const _hoisted_85 = {
  key: 1,
  class: "text-center py-8"
};
const _hoisted_86 = { class: "text-gray-600" };
const _hoisted_87 = {
  key: 2,
  class: "space-y-4"
};
const _hoisted_88 = { class: "grid grid-cols-1 md:grid-cols-4 gap-4" };
const _hoisted_89 = { class: "text-sm text-gray-900 font-mono" };
const _hoisted_90 = { class: "text-sm text-gray-900" };
const _hoisted_91 = { class: "text-sm text-gray-900 font-semibold" };
const _hoisted_92 = {
  key: 0,
  class: "mt-3 pt-3 border-t border-gray-100"
};
const _hoisted_93 = { class: "text-sm text-gray-900" };
const _hoisted_94 = { class: "px-6 py-4 border-t border-gray-200 flex justify-end" };
const _sfc_main = {
  __name: "Scanner",
  setup(__props) {
    const selectedFile = ref(null);
    const selectedFileName = ref("");
    const capturedDataUrl = ref("");
    const extractError = ref("");
    const extracting = ref(false);
    const invoice = ref(null);
    const submitting = ref(false);
    const scannerConfig = reactive({
      connectionUrl: "http://localhost:17890",
      dpi: 300
    });
    const isDragOver = ref(false);
    const isFinalPhotoDragOver = ref(false);
    const scanning = ref(false);
    const scannedImageBlob = ref(null);
    const scannedImageUrl = ref("");
    const imagePreviewUrl = computed(() => {
      if (selectedFile.value) return URL.createObjectURL(selectedFile.value);
      if (capturedDataUrl.value) return capturedDataUrl.value;
      if (scannedImageBlob.value) return URL.createObjectURL(scannedImageBlob.value);
      if (scannedImageUrl.value) return scannedImageUrl.value;
      return null;
    });
    const finalPhotoPreviewUrl = computed(() => {
      if (finalize.finalPhotoFile) return URL.createObjectURL(finalize.finalPhotoFile);
      return null;
    });
    const finalize = reactive({
      type: "purchase",
      // default purchase
      billAmount: null,
      finalPhotoFile: null,
      supplierName: "bntl",
      items: [],
      isReturn: false
      // New field for return/credit note
    });
    const deletedRows = ref([]);
    const itemValidation = ref(null);
    const showNewItemDialog = ref(false);
    const newItemData = reactive({
      item_code: "",
      item_name: "",
      selling_price: 0,
      valuation_price: 0,
      uom_conversion: 6,
      // Default CS = 6 Nos
      rowIndex: -1
    });
    const invoiceType = ref("");
    const isProcessing = ref(false);
    const detectionMethod = ref("");
    const showLastInvoicesDialog = ref(false);
    const loadingLastInvoices = ref(false);
    const lastInvoices = ref([]);
    const onFileSelected = (e) => {
      var _a, _b;
      const f = (_b = (_a = e == null ? void 0 : e.target) == null ? void 0 : _a.files) == null ? void 0 : _b[0];
      if (!f) return;
      selectedFile.value = f;
      selectedFileName.value = f.name;
      capturedDataUrl.value = "";
    };
    const onFinalPhotoSelected = (e) => {
      var _a, _b;
      const f = (_b = (_a = e == null ? void 0 : e.target) == null ? void 0 : _a.files) == null ? void 0 : _b[0];
      if (f) finalize.finalPhotoFile = f;
    };
    const onDrop = (e) => {
      e.preventDefault();
      isDragOver.value = false;
      const files = Array.from(e.dataTransfer.files);
      const imageFile = files.find((file) => file.type.startsWith("image/"));
      if (imageFile) {
        selectedFile.value = imageFile;
        selectedFileName.value = imageFile.name;
        capturedDataUrl.value = "";
        scannedImageBlob.value = null;
        scannedImageUrl.value = "";
      }
    };
    const onDragLeave = () => {
      isDragOver.value = false;
    };
    const onFinalPhotoDrop = (e) => {
      e.preventDefault();
      isFinalPhotoDragOver.value = false;
      const files = Array.from(e.dataTransfer.files);
      const imageFile = files.find((file) => file.type.startsWith("image/"));
      if (imageFile) {
        finalize.finalPhotoFile = imageFile;
      }
    };
    const onFinalPhotoDragLeave = () => {
      isFinalPhotoDragOver.value = false;
    };
    const scan = () => __async(this, null, function* () {
      try {
        scanning.value = true;
        const res = yield fetch(`${scannerConfig.connectionUrl}/scan`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            dpi: scannerConfig.dpi,
            mode: "Color"
          })
        });
        if (!res.ok) {
          const error = yield res.text();
          throw new Error(`Scan failed: ${error}`);
        }
        const { data, format } = yield res.json();
        const byteArray = Uint8Array.from(atob(data), (c) => c.charCodeAt(0));
        const imageBlob = new Blob([byteArray], { type: `image/${format}` });
        scannedImageBlob.value = imageBlob;
        scannedImageUrl.value = URL.createObjectURL(imageBlob);
        console.log("Scan completed:", {
          scannedImageBlob: !!scannedImageBlob.value,
          scannedImageUrl: !!scannedImageUrl.value,
          imagePreviewUrl: imagePreviewUrl.value,
          canExtract: canExtract.value
        });
        selectedFile.value = null;
        selectedFileName.value = "";
        capturedDataUrl.value = "";
        alert("Document scanned successfully!");
      } catch (err) {
        alert("Scan failed: " + err.message);
      } finally {
        scanning.value = false;
      }
    });
    const scanFinalPhoto = () => __async(this, null, function* () {
      try {
        scanning.value = true;
        const res = yield fetch(`${scannerConfig.connectionUrl}/scan`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            dpi: scannerConfig.dpi,
            mode: "Color"
          })
        });
        if (!res.ok) {
          const error = yield res.text();
          throw new Error(`Scan failed: ${error}`);
        }
        const { data, format } = yield res.json();
        const byteArray = Uint8Array.from(atob(data), (c) => c.charCodeAt(0));
        const imageBlob = new Blob([byteArray], { type: `image/${format}` });
        finalize.finalPhotoFile = new File([imageBlob], `scanned_photo.${format}`, { type: `image/${format}` });
        alert("Photo scanned successfully!");
      } catch (err) {
        alert("Scan failed: " + err.message);
      } finally {
        scanning.value = false;
      }
    });
    const clearImage = () => {
      if (scannedImageUrl.value) {
        URL.revokeObjectURL(scannedImageUrl.value);
      }
      selectedFile.value = null;
      selectedFileName.value = "";
      capturedDataUrl.value = "";
      scannedImageBlob.value = null;
      scannedImageUrl.value = "";
      if (window.gc) {
        window.gc();
      }
    };
    const clearFinalPhoto = () => {
      if (finalize.finalPhotoFile) {
        finalize.finalPhotoFile = null;
      }
      if (window.gc) {
        window.gc();
      }
    };
    const canExtract = computed(() => {
      return !!selectedFile.value || !!capturedDataUrl.value || !!scannedImageBlob.value || !!scannedImageUrl.value;
    });
    const safeJson = (res) => __async(this, null, function* () {
      try {
        const text = yield res.text();
        if (!text) return {};
        try {
          return JSON.parse(text);
        } catch (_) {
        }
        const cleaned = text.trim().replace(/^```(?:json)?/i, "").replace(/```$/, "");
        return JSON.parse(cleaned);
      } catch (e) {
        return {};
      }
    });
    const memoryMonitor = {
      checkMemoryUsage: () => {
        if ("memory" in performance) {
          const memory = performance.memory;
          const usedMB = Math.round(memory.usedJSHeapSize / 1024 / 1024);
          const totalMB = Math.round(memory.totalJSHeapSize / 1024 / 1024);
          const limitMB = Math.round(memory.jsHeapSizeLimit / 1024 / 1024);
          console.log(`Memory Usage: ${usedMB}MB / ${totalMB}MB (${limitMB}MB limit)`);
          if (usedMB > limitMB * 0.8) {
            console.warn("High memory usage detected! Consider clearing some data.");
            return false;
          }
          return true;
        }
        return true;
      },
      forceCleanup: () => {
        if (window.gc) {
          window.gc();
        }
        try {
          localStorage.clear();
          sessionStorage.clear();
        } catch (e) {
          console.warn("Could not clear storage:", e);
        }
      }
    };
    const robustFetch = (_0, ..._1) => __async(this, [_0, ..._1], function* (url, opts = {}) {
      const maxRetries = 2;
      const retryDelays = [500, 1e3];
      for (let attempt = 0; attempt <= maxRetries; attempt++) {
        try {
          if (!memoryMonitor.checkMemoryUsage()) {
            memoryMonitor.forceCleanup();
          }
          const controller = new AbortController();
          const timeout = setTimeout(() => controller.abort(), 3e4);
          const res = yield fetch(url, __spreadProps(__spreadValues({}, opts), { signal: controller.signal }));
          clearTimeout(timeout);
          if ([502, 503, 504].includes(res.status) && attempt < maxRetries) {
            yield new Promise((r) => setTimeout(r, retryDelays[attempt]));
            continue;
          }
          return res;
        } catch (e) {
          if (attempt < maxRetries) {
            yield new Promise((r) => setTimeout(r, retryDelays[attempt]));
            continue;
          }
          throw new Error((e == null ? void 0 : e.name) === "AbortError" ? "Request timed out. Please try again." : (e == null ? void 0 : e.message) || "Network error");
        }
      }
    });
    const extractInvoice = () => __async(this, null, function* () {
      var _a, _b, _c, _d, _e, _f, _g, _h;
      extractError.value = "";
      extracting.value = true;
      invoice.value = null;
      invoiceType.value = "";
      finalize.isReturn = false;
      detectionMethod.value = "";
      try {
        if (!finalize.type) throw new Error("Select invoice type first");
        let res;
        if (selectedFile.value) {
          const b64 = yield toBase64(selectedFile.value);
          res = yield robustFetch("/api/method/custom_erp.custom_erp.purchase_invoice.api.extract_invoice", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image_data: b64 })
          });
        } else if (capturedDataUrl.value) {
          res = yield robustFetch("/api/method/custom_erp.custom_erp.purchase_invoice.api.extract_invoice", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image_data: capturedDataUrl.value })
          });
        } else if (scannedImageBlob.value) {
          const b64 = yield toBase64(scannedImageBlob.value);
          res = yield robustFetch("/api/method/custom_erp.custom_erp.purchase_invoice.api.extract_invoice", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image_data: b64 })
          });
        } else {
          throw new Error("No input");
        }
        const data = yield safeJson(res);
        const msg = data.message || data;
        if (!res.ok || !(msg == null ? void 0 : msg.success)) throw new Error((msg == null ? void 0 : msg.error) || "Extraction failed");
        console.log("Full extraction response:", msg);
        console.log("Extracted data:", msg.data);
        const title = ((_a = msg.data) == null ? void 0 : _a.title) || "";
        console.log("Extracted title:", title);
        let detectedType = null;
        let method = "inferred";
        if (title.toLowerCase().includes("credit note")) {
          detectedType = "credit_note";
          method = "title";
          console.log("Detected Credit Note from title");
        } else if (title.toLowerCase().includes("tax invoice")) {
          detectedType = "tax_invoice";
          method = "title";
          console.log("Detected Tax Invoice from title");
        }
        if (!detectedType) {
          console.log("Title detection failed, trying to infer from other fields...");
          const hasNegativeValues = (_c = (_b = msg.data) == null ? void 0 : _b.items) == null ? void 0 : _c.some(
            (item) => item.lineTotal && item.lineTotal < 0
          );
          if (hasNegativeValues) {
            detectedType = "credit_note";
            method = "inferred";
            console.log("Inferred Credit Note from negative line totals");
          } else {
            detectedType = "tax_invoice";
            method = "inferred";
            console.log("Defaulting to Tax Invoice");
          }
        }
        invoiceType.value = detectedType;
        finalize.isReturn = detectedType === "credit_note";
        detectionMethod.value = method;
        console.log("Final decision:", {
          detectedType,
          isReturn: finalize.isReturn,
          title,
          method
        });
        invoice.value = {
          invoiceNumber: ((_d = msg.data) == null ? void 0 : _d.invoiceNumber) || "",
          invoiceDate: normalizeDateToISO(((_e = msg.data) == null ? void 0 : _e.invoiceDate) || ""),
          customerName: "bntl",
          items: Array.isArray((_f = msg.data) == null ? void 0 : _f.items) ? msg.data.items.map((it) => ({
            materialCode: it.materialCode || it.materialDescription || "",
            materialDescription: it.materialDescription || it.materialCode || "",
            salesQty: Math.abs(Number(it.salesQty || 0)),
            // Always make quantity positive
            uom: it.uom || "CS",
            unitPrice: it.unitPrice,
            lineTotal: it.lineTotal,
            isMissing: false,
            itemCreated: false
          })) : [],
          totalAmount: Number(((_g = msg.data) == null ? void 0 : _g.totalAmount) || 0),
          totalDiscountAmount: Number(((_h = msg.data) == null ? void 0 : _h.totalDiscountAmount) || 0)
        };
        finalize.items = (invoice.value.items || []).map(() => ({ leakages: 0, bursts: 0 }));
        finalize.type = finalize.type || msg.invoiceType || "purchase";
        if (invoice.value.totalAmount && (finalize.billAmount === null || finalize.billAmount === void 0)) {
          finalize.billAmount = invoice.value.totalAmount;
        }
      } catch (e) {
        extractError.value = (e == null ? void 0 : e.message) || "Failed to extract invoice";
      } finally {
        extracting.value = false;
      }
    });
    const toBase64 = (file) => new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        const result = String(reader.result);
        reader.onload = null;
        reader.onerror = null;
        resolve(result);
      };
      reader.onerror = (error) => {
        reader.onload = null;
        reader.onerror = null;
        reject(error);
      };
      reader.readAsDataURL(file);
    });
    function normalizeDateToISO(input) {
      if (!input) return (/* @__PURE__ */ new Date()).toISOString().slice(0, 10);
      if (/^\d{4}-\d{2}-\d{2}$/.test(input)) return input;
      let m = input.match(/^(\d{1,2})[\/.\-](\d{1,2})[\/.\-](\d{4})$/);
      if (m) {
        const d = m[1].padStart(2, "0");
        const mo = m[2].padStart(2, "0");
        const y = m[3];
        return `${y}-${mo}-${d}`;
      }
      m = input.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
      if (m) {
        const mo = m[1].padStart(2, "0");
        const d = m[2].padStart(2, "0");
        const y = m[3];
        return `${y}-${mo}-${d}`;
      }
      const t = Date.parse(input);
      if (!isNaN(t)) return new Date(t).toISOString().slice(0, 10);
      return (/* @__PURE__ */ new Date()).toISOString().slice(0, 10);
    }
    const parseMsg = (obj) => {
      var _a;
      return obj && ((_a = obj.message) != null ? _a : obj) || {};
    };
    const submitInvoice = () => __async(this, null, function* () {
      var _a, _b;
      if (!invoice.value || !finalize.type || isProcessing.value) return;
      isProcessing.value = true;
      submitting.value = true;
      try {
        if (!memoryMonitor.checkMemoryUsage()) {
          memoryMonitor.forceCleanup();
        }
        const payload = {
          invoiceNumber: invoice.value.invoiceNumber,
          invoiceDate: invoice.value.invoiceDate,
          customerName: "bntl",
          supplier: finalize.supplierName || "bntl",
          discount_amount: invoice.value.totalDiscountAmount || 0,
          isReturn: finalize.isReturn,
          items: []
        };
        const items = invoice.value.items || [];
        for (let i = 0; i < items.length; i++) {
          const it = items[i];
          const item = {
            materialCode: it.materialCode,
            materialDescription: it.materialDescription,
            salesQty: it.salesQty,
            uom: it.uom,
            unitPrice: it.unitPrice,
            lineTotal: it.lineTotal
          };
          if (finalize.type === "purchase") {
            item.leakages = ((_a = finalize.items[i]) == null ? void 0 : _a.leakages) || 0;
            item.bursts = ((_b = finalize.items[i]) == null ? void 0 : _b.bursts) || 0;
          }
          payload.items.push(item);
        }
        if (finalize.type === "purchase") {
          if (finalize.billAmount) payload.cust_bill_actual_amount = finalize.billAmount;
          if (finalize.finalPhotoFile) {
            payload.photo_base64 = yield toBase64(finalize.finalPhotoFile);
          }
        }
        if (!memoryMonitor.checkMemoryUsage()) {
          memoryMonitor.forceCleanup();
        }
        let res;
        if (finalize.type === "purchase") {
          res = yield robustFetch("/api/method/custom_erp.custom_erp.purchase_invoice.api.create_purchase_invoice", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ payload })
          });
        } else {
          res = yield robustFetch("/api/method/custom_erp.custom_erp.sales_invoice.api.create_sales_invoice", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ payload })
          });
        }
        const raw = yield safeJson(res);
        const j = parseMsg(raw);
        if (!res.ok || !(j == null ? void 0 : j.success)) {
          throw new Error((j == null ? void 0 : j.error) || `Failed to create ${finalize.type === "purchase" ? "Purchase" : "Sales"} Invoice`);
        }
        window.alert(`${finalize.type === "purchase" ? "Purchase" : "Sales"} Invoice Created: ${j == null ? void 0 : j.name}`);
        payload.items = null;
        if (payload.photo_base64) {
          payload.photo_base64 = null;
        }
        memoryMonitor.forceCleanup();
      } catch (e) {
        try {
          const verify = yield checkForDuplicateInvoice(true);
          if (verify == null ? void 0 : verify.existingName) {
            window.alert(`${finalize.type === "purchase" ? "Purchase" : "Sales"} Invoice Created: ${verify.existingName}`);
          } else {
            throw new Error((e == null ? void 0 : e.message) || "Failed");
          }
        } catch (vErr) {
          window.alert(`Error: ${(e == null ? void 0 : e.message) || "Failed"}`);
        }
      } finally {
        submitting.value = false;
        isProcessing.value = false;
        memoryMonitor.forceCleanup();
      }
    });
    const validateItems = () => __async(this, null, function* () {
      var _a;
      try {
        invoice.value.items.forEach((item) => {
          item.isMissing = false;
          item.itemCreated = false;
        });
        console.log("Sending items for validation:", invoice.value.items);
        console.log("Items type:", typeof invoice.value.items);
        console.log("Items length:", (_a = invoice.value.items) == null ? void 0 : _a.length);
        console.log("JSON stringified:", JSON.stringify(invoice.value.items));
        console.log("Final request body:", JSON.stringify({ items: JSON.stringify(invoice.value.items) }));
        const res = yield robustFetch("/api/method/custom_erp.custom_erp.purchase_invoice.api.validate_items_master", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ items: JSON.stringify(invoice.value.items) })
        });
        console.log("Validation response status:", res.status);
        const data = yield safeJson(res);
        console.log("Validation response data:", data);
        const msg = data.message || data;
        if (!res.ok || !msg.success) throw new Error(msg.error || "Validation failed");
        if (msg.validation && msg.validation.missing_items) {
          msg.validation.missing_items.forEach((missingItem) => {
            const item = invoice.value.items.find((it) => it.materialCode === missingItem.materialCode);
            if (item) {
              item.isMissing = true;
            }
          });
        }
        itemValidation.value = msg.validation;
        return msg.validation;
      } catch (e) {
        console.error("Validation error:", e);
        window.alert(`Validation error: ${(e == null ? void 0 : e.message) || "Failed to validate items"}`);
        return { all_valid: false, missing_items: [], valid_items: [] };
      }
    });
    const showMissingItemsDialog = (missingItems) => {
      invoice.value.items.forEach((item, index) => {
        const isMissing = missingItems.some((missing) => missing.materialCode === item.materialCode);
        item.isMissing = isMissing;
      });
      const missingCodes = missingItems.map((item) => item.materialCode).join(", ");
      window.confirm(
        `The following items are not found in master data:

${missingCodes}

Please add them as new items using the "+" button, or correct the item codes if there are typos.`
      );
    };
    const openNewItemDialog = (rowIndex) => {
      const item = invoice.value.items[rowIndex];
      newItemData.item_code = item.materialCode;
      newItemData.item_name = item.materialDescription;
      newItemData.rowIndex = rowIndex;
      newItemData.selling_price = item.unitPrice || 0;
      newItemData.valuation_price = item.unitPrice || 0;
      newItemData.uom_conversion = item.uom === "CS" ? 6 : 1;
      showNewItemDialog.value = true;
    };
    const createNewItem = () => __async(this, null, function* () {
      try {
        const res = yield fetch("/api/method/custom_erp.custom_erp.purchase_invoice.api.create_new_item_for_invoice", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ item_data: JSON.stringify(newItemData) })
        });
        const data = yield safeJson(res);
        const msg = data.message || data;
        if (!res.ok || !msg.success) throw new Error(msg.error || "Failed to create item");
        const rowIndex = newItemData.rowIndex;
        if (rowIndex >= 0 && rowIndex < invoice.value.items.length) {
          invoice.value.items[rowIndex].isMissing = false;
          invoice.value.items[rowIndex].itemCreated = true;
        }
        showNewItemDialog.value = false;
        window.alert(`Item created successfully: ${msg.item_code}`);
        yield validateItems();
      } catch (e) {
        window.alert(`Error creating item: ${(e == null ? void 0 : e.message) || "Failed"}`);
      }
    });
    const resetItemStatuses = () => {
      invoice.value.items.forEach((item) => {
        item.isMissing = false;
        item.itemCreated = false;
      });
      itemValidation.value = null;
    };
    const checkForDuplicateInvoice = (returnName = false) => __async(this, null, function* () {
      try {
        const apiEndpoint = finalize.type === "purchase" ? "/api/method/custom_erp.custom_erp.purchase_invoice.api.check_duplicate_invoice" : "/api/method/custom_erp.custom_erp.sales_invoice.api.check_duplicate_invoice";
        const res = yield robustFetch(apiEndpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            supplier: finalize.supplierName,
            customer: finalize.supplierName,
            invoice_number: invoice.value.invoiceNumber,
            invoice_date: invoice.value.invoiceDate,
            invoice_type: finalize.type
          })
        });
        const raw = yield safeJson(res);
        const msg = parseMsg(raw);
        if (!res.ok) return { isDuplicate: false };
        return { isDuplicate: !!msg.isDuplicate, existingName: msg.existing_invoice || null };
      } catch (e) {
        return { isDuplicate: false };
      }
    });
    const deleteRow = (index) => {
      var _a;
      if (!((_a = invoice.value) == null ? void 0 : _a.items) || index < 0 || index >= invoice.value.items.length) return;
      const deletedRow = {
        index,
        item: __spreadValues({}, invoice.value.items[index]),
        finalizeItem: __spreadValues({}, finalize.items[index])
      };
      invoice.value.items.splice(index, 1);
      finalize.items.splice(index, 1);
      deletedRows.value.push(deletedRow);
    };
    const undoLastDelete = () => {
      if (deletedRows.value.length === 0) return;
      const lastDeleted = deletedRows.value.pop();
      invoice.value.items.splice(lastDeleted.index, 0, lastDeleted.item);
      finalize.items.splice(lastDeleted.index, 0, lastDeleted.finalizeItem);
    };
    const showLastInvoices = () => __async(this, null, function* () {
      if (!finalize.type) {
        window.alert("Please select an invoice type first");
        return;
      }
      showLastInvoicesDialog.value = true;
      yield fetchLastInvoices();
    });
    const fetchLastInvoices = () => __async(this, null, function* () {
      loadingLastInvoices.value = true;
      lastInvoices.value = [];
      try {
        const apiEndpoint = finalize.type === "purchase" ? "/api/method/custom_erp.custom_erp.purchase_invoice.api.get_last_invoices" : "/api/method/custom_erp.custom_erp.sales_invoice.api.get_last_invoices";
        const res = yield robustFetch(apiEndpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ limit: 3 })
        });
        const data = yield safeJson(res);
        const msg = data.message || data;
        if (!res.ok || !(msg == null ? void 0 : msg.success)) {
          throw new Error((msg == null ? void 0 : msg.error) || "Failed to fetch invoices");
        }
        lastInvoices.value = msg.invoices || [];
      } catch (e) {
        console.error("Error fetching last invoices:", e);
        window.alert(`Error fetching invoices: ${(e == null ? void 0 : e.message) || "Failed to fetch invoices"}`);
      } finally {
        loadingLastInvoices.value = false;
      }
    });
    const formatDate = (dateString) => {
      if (!dateString) return "N/A";
      try {
        const date = new Date(dateString);
        return date.toLocaleDateString("en-IN", {
          year: "numeric",
          month: "short",
          day: "numeric"
        });
      } catch (e) {
        return dateString;
      }
    };
    const formatAmount = (amount) => {
      if (!amount && amount !== 0) return "0.00";
      return Number(amount).toLocaleString("en-IN", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    };
    const getStatusClass = (docstatus) => {
      switch (docstatus) {
        case 0:
          return "bg-yellow-100 text-yellow-800";
        case 1:
          return "bg-green-100 text-green-800";
        case 2:
          return "bg-red-100 text-red-800";
        default:
          return "bg-gray-100 text-gray-800";
      }
    };
    const getStatusText = (docstatus) => {
      switch (docstatus) {
        case 0:
          return "Draft";
        case 1:
          return "Submitted";
        case 2:
          return "Cancelled";
        default:
          return "Unknown";
      }
    };
    watch([scannedImageBlob, scannedImageUrl], () => {
      console.log("Scanned image changed:", {
        scannedImageBlob: !!scannedImageBlob.value,
        scannedImageUrl: !!scannedImageUrl.value,
        imagePreviewUrl: imagePreviewUrl.value,
        canExtract: canExtract.value
      });
    });
    onMounted(() => {
    });
    const confirmAndSubmit = () => __async(this, null, function* () {
      var _a;
      if (!invoice.value || isProcessing.value) return;
      const validationResult = yield validateItems();
      if (!(validationResult == null ? void 0 : validationResult.all_valid)) {
        showMissingItemsDialog((validationResult == null ? void 0 : validationResult.missing_items) || []);
        return;
      }
      const dup = yield checkForDuplicateInvoice(true);
      if (dup == null ? void 0 : dup.isDuplicate) {
        const proceedDup = window.confirm(
          `A ${finalize.type} invoice already exists with the same details.

Supplier: ${finalize.supplierName}
Invoice No: ${invoice.value.invoiceNumber}
Date: ${invoice.value.invoiceDate}
${dup.existingName ? `Existing: ${dup.existingName}
` : ""}Do you want to create it anyway?`
        );
        if (!proceedDup) return;
      }
      const lines = [
        `Type: ${finalize.type}`,
        `Purchase Invoice Type: ${finalize.isReturn ? "Credit Note (Return)" : "Tax Invoice (Regular)"}`,
        `Invoice No: ${invoice.value.invoiceNumber}`,
        `Date: ${invoice.value.invoiceDate}`,
        `Party: ${invoice.value.customerName}`,
        `Items: ${invoice.value.items.length}`,
        `Billed Actual Total: ${(_a = finalize.billAmount) != null ? _a : ""}`
      ];
      const ok = window.confirm(`Confirm create ${finalize.type} invoice?

` + lines.join("\n"));
      if (!ok) return;
      yield submitInvoice();
    });
    return (_ctx, _cache) => {
      var _a, _b;
      const _component_Button = resolveComponent("Button");
      const _component_Alert = resolveComponent("Alert");
      return openBlock(), createElementBlock(Fragment, null, [
        createBaseVNode("div", _hoisted_1, [
          createBaseVNode("div", _hoisted_2, [
            createBaseVNode("div", _hoisted_3, [
              createBaseVNode("div", _hoisted_4, [
                createBaseVNode("div", null, [
                  _cache[22] || (_cache[22] = createBaseVNode("h1", { class: "text-2xl font-bold text-gray-900" }, "Invoice Scanner", -1)),
                  createBaseVNode("p", _hoisted_5, "Authenticated as " + toDisplayString(unref(session).user), 1)
                ]),
                createVNode(_component_Button, {
                  onClick: _cache[0] || (_cache[0] = ($event) => unref(session).logout.submit()),
                  theme: "gray",
                  variant: "outline"
                }, {
                  default: withCtx(() => _cache[23] || (_cache[23] = [
                    createTextVNode("Logout")
                  ])),
                  _: 1,
                  __: [23]
                })
              ])
            ])
          ]),
          createBaseVNode("div", _hoisted_6, [
            createBaseVNode("div", _hoisted_7, [
              _cache[32] || (_cache[32] = createBaseVNode("h2", { class: "text-lg font-semibold text-gray-900 mb-4" }, "Invoice Image Input", -1)),
              createBaseVNode("div", _hoisted_8, [
                _cache[26] || (_cache[26] = createBaseVNode("label", { class: "block text-sm text-gray-700 mb-2" }, "Invoice Type", -1)),
                createBaseVNode("div", _hoisted_9, [
                  createBaseVNode("label", _hoisted_10, [
                    withDirectives(createBaseVNode("input", {
                      type: "radio",
                      value: "purchase",
                      "onUpdate:modelValue": _cache[1] || (_cache[1] = ($event) => finalize.type = $event)
                    }, null, 512), [
                      [vModelRadio, finalize.type]
                    ]),
                    _cache[24] || (_cache[24] = createTextVNode(" Purchase "))
                  ]),
                  createBaseVNode("label", _hoisted_11, [
                    withDirectives(createBaseVNode("input", {
                      type: "radio",
                      value: "sales",
                      "onUpdate:modelValue": _cache[2] || (_cache[2] = ($event) => finalize.type = $event)
                    }, null, 512), [
                      [vModelRadio, finalize.type]
                    ]),
                    _cache[25] || (_cache[25] = createTextVNode(" Sales "))
                  ])
                ])
              ]),
              createBaseVNode("div", _hoisted_12, [
                createBaseVNode("div", null, [
                  _cache[27] || (_cache[27] = createBaseVNode("label", { class: "block text-sm font-medium text-gray-700 mb-2" }, "Connection URL", -1)),
                  withDirectives(createBaseVNode("input", {
                    type: "text",
                    "onUpdate:modelValue": _cache[3] || (_cache[3] = ($event) => scannerConfig.connectionUrl = $event),
                    class: "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    placeholder: "http://localhost:17890"
                  }, null, 512), [
                    [vModelText, scannerConfig.connectionUrl]
                  ])
                ]),
                createBaseVNode("div", null, [
                  _cache[28] || (_cache[28] = createBaseVNode("label", { class: "block text-sm font-medium text-gray-700 mb-2" }, "DPI", -1)),
                  withDirectives(createBaseVNode("input", {
                    type: "number",
                    "onUpdate:modelValue": _cache[4] || (_cache[4] = ($event) => scannerConfig.dpi = $event),
                    min: "100",
                    max: "600",
                    step: "50",
                    class: "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                    placeholder: "300"
                  }, null, 512), [
                    [
                      vModelText,
                      scannerConfig.dpi,
                      void 0,
                      { number: true }
                    ]
                  ])
                ])
              ]),
              createBaseVNode("div", {
                class: normalizeClass(["border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-blue-400 transition-colors", { "border-blue-400 bg-blue-50": isDragOver.value }]),
                onDrop,
                onDragover: _cache[5] || (_cache[5] = withModifiers(() => {
                }, ["prevent"])),
                onDragenter: _cache[6] || (_cache[6] = () => isDragOver.value = true),
                onDragleave: onDragLeave
              }, [
                selectedFile.value || capturedDataUrl.value || scannedImageBlob.value || scannedImageUrl.value ? (openBlock(), createElementBlock("div", _hoisted_13, [
                  imagePreviewUrl.value ? (openBlock(), createElementBlock("img", {
                    key: 0,
                    src: imagePreviewUrl.value,
                    alt: "Invoice Preview",
                    class: "max-w-full h-auto max-h-64 mx-auto rounded-lg shadow-md"
                  }, null, 8, _hoisted_14)) : createCommentVNode("", true),
                  createBaseVNode("div", { class: "mt-2 flex justify-center space-x-2" }, [
                    createBaseVNode("button", {
                      onClick: clearImage,
                      class: "px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded"
                    }, " Remove Image ")
                  ])
                ])) : createCommentVNode("", true),
                !selectedFile.value && !capturedDataUrl.value && !scannedImageBlob.value && !scannedImageUrl.value ? (openBlock(), createElementBlock("div", _hoisted_15, [
                  createBaseVNode("div", _hoisted_16, [
                    createBaseVNode("label", _hoisted_17, [
                      createBaseVNode("input", {
                        type: "file",
                        onChange: onFileSelected,
                        accept: "image/*",
                        class: "hidden"
                      }, null, 32),
                      _cache[29] || (_cache[29] = createBaseVNode("div", { class: "px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-center" }, " 📁 Upload from Local Storage ", -1))
                    ]),
                    createBaseVNode("button", {
                      onClick: scan,
                      disabled: scanning.value,
                      class: "flex-1 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
                    }, [
                      scanning.value ? (openBlock(), createElementBlock("span", _hoisted_19, "🔄 Scanning...")) : (openBlock(), createElementBlock("span", _hoisted_20, "📷 Scan Document"))
                    ], 8, _hoisted_18)
                  ]),
                  _cache[30] || (_cache[30] = createBaseVNode("div", { class: "text-gray-500 text-sm" }, [
                    createBaseVNode("p", null, "Or drag and drop an image file here"),
                    createBaseVNode("p", { class: "text-xs mt-1" }, "Supports: JPG, PNG, WebP")
                  ], -1))
                ])) : createCommentVNode("", true)
              ], 34),
              createBaseVNode("div", _hoisted_21, [
                createVNode(_component_Button, {
                  theme: "blue",
                  loading: extracting.value,
                  onClick: extractInvoice,
                  disabled: !canExtract.value
                }, {
                  default: withCtx(() => _cache[31] || (_cache[31] = [
                    createTextVNode("Extract Invoice")
                  ])),
                  _: 1,
                  __: [31]
                }, 8, ["loading", "disabled"]),
                createVNode(_component_Button, {
                  theme: "gray",
                  variant: "outline",
                  onClick: showLastInvoices,
                  loading: loadingLastInvoices.value
                }, {
                  default: withCtx(() => [
                    createTextVNode(" View Last 3 " + toDisplayString(finalize.type === "purchase" ? "Purchase" : "Sales") + " Invoices ", 1)
                  ]),
                  _: 1
                }, 8, ["loading"]),
                extractError.value ? (openBlock(), createBlock(_component_Alert, {
                  key: 0,
                  theme: "red"
                }, {
                  default: withCtx(() => [
                    createTextVNode(toDisplayString(extractError.value), 1)
                  ]),
                  _: 1
                })) : createCommentVNode("", true)
              ])
            ]),
            invoice.value ? (openBlock(), createElementBlock("div", _hoisted_22, [
              _cache[52] || (_cache[52] = createBaseVNode("h2", { class: "text-lg font-semibold text-gray-900 mb-4" }, "Extracted Data", -1)),
              invoiceType.value ? (openBlock(), createElementBlock("div", {
                key: 0,
                class: normalizeClass(["mb-4 p-3 rounded-md", invoiceType.value === "credit_note" ? "bg-orange-50 border border-orange-200" : "bg-blue-50 border border-blue-200"])
              }, [
                createBaseVNode("div", _hoisted_23, [
                  invoiceType.value === "credit_note" ? (openBlock(), createElementBlock("div", _hoisted_24, " ↶ ")) : (openBlock(), createElementBlock("div", _hoisted_25, " 📄 ")),
                  createBaseVNode("div", _hoisted_26, [
                    createBaseVNode("p", {
                      class: normalizeClass(["text-sm font-medium", invoiceType.value === "credit_note" ? "text-orange-800" : "text-blue-800"])
                    }, toDisplayString(invoiceType.value === "credit_note" ? "Credit Note (Return)" : "Tax Invoice (Regular)"), 3),
                    createBaseVNode("p", {
                      class: normalizeClass(["text-sm", invoiceType.value === "credit_note" ? "text-orange-700" : "text-blue-700"])
                    }, toDisplayString(invoiceType.value === "credit_note" ? "This is a return/credit note. Will be processed as a return transaction." : "This is a regular tax invoice."), 3),
                    createBaseVNode("p", _hoisted_27, toDisplayString(detectionMethod.value === "title" ? `Detected from document title: "${_ctx.title}"` : "Inferred from document content"), 1)
                  ])
                ])
              ], 2)) : createCommentVNode("", true),
              createBaseVNode("div", _hoisted_28, [
                createBaseVNode("div", null, [
                  _cache[33] || (_cache[33] = createBaseVNode("label", { class: "block text-sm text-gray-600 mb-1" }, "Invoice Number", -1)),
                  withDirectives(createBaseVNode("input", {
                    "onUpdate:modelValue": _cache[7] || (_cache[7] = ($event) => invoice.value.invoiceNumber = $event),
                    class: "w-full px-3 py-2 border rounded",
                    placeholder: "INV-001"
                  }, null, 512), [
                    [vModelText, invoice.value.invoiceNumber]
                  ])
                ]),
                createBaseVNode("div", null, [
                  _cache[34] || (_cache[34] = createBaseVNode("label", { class: "block text-sm text-gray-600 mb-1" }, "Invoice Date", -1)),
                  withDirectives(createBaseVNode("input", {
                    "onUpdate:modelValue": _cache[8] || (_cache[8] = ($event) => invoice.value.invoiceDate = $event),
                    type: "date",
                    class: "w-full px-3 py-2 border rounded"
                  }, null, 512), [
                    [vModelText, invoice.value.invoiceDate]
                  ])
                ]),
                createBaseVNode("div", null, [
                  _cache[35] || (_cache[35] = createBaseVNode("label", { class: "block text-sm text-gray-600 mb-1" }, "Supplier", -1)),
                  withDirectives(createBaseVNode("input", {
                    "onUpdate:modelValue": _cache[9] || (_cache[9] = ($event) => finalize.supplierName = $event),
                    class: "w-full px-3 py-2 border rounded",
                    placeholder: "bntl"
                  }, null, 512), [
                    [vModelText, finalize.supplierName]
                  ])
                ])
              ]),
              createBaseVNode("div", _hoisted_29, [
                createBaseVNode("div", null, [
                  _cache[36] || (_cache[36] = createBaseVNode("label", { class: "block text-sm text-gray-700 mb-2" }, "Bill Actual Amount", -1)),
                  withDirectives(createBaseVNode("input", {
                    type: "number",
                    step: "0.01",
                    class: "w-full px-3 py-2 border rounded",
                    "onUpdate:modelValue": _cache[10] || (_cache[10] = ($event) => finalize.billAmount = $event)
                  }, null, 512), [
                    [
                      vModelText,
                      finalize.billAmount,
                      void 0,
                      { number: true }
                    ]
                  ])
                ]),
                createBaseVNode("div", null, [
                  _cache[38] || (_cache[38] = createBaseVNode("label", { class: "block text-sm text-gray-700 mb-2" }, "Purchase Invoice Type", -1)),
                  createBaseVNode("div", _hoisted_30, [
                    withDirectives(createBaseVNode("input", {
                      type: "checkbox",
                      "onUpdate:modelValue": _cache[11] || (_cache[11] = ($event) => finalize.isReturn = $event),
                      class: "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 focus:ring-2"
                    }, null, 512), [
                      [vModelCheckbox, finalize.isReturn]
                    ]),
                    _cache[37] || (_cache[37] = createBaseVNode("label", { class: "ml-2 text-sm text-gray-700" }, "Mark as Credit Note (Return)", -1))
                  ]),
                  createBaseVNode("p", _hoisted_31, " When checked, will be processed as a return transaction. " + toDisplayString(detectionMethod.value === "title" ? "Auto-detected from document title." : "Auto-detected from document content. Please verify."), 1),
                  detectionMethod.value === "inferred" ? (openBlock(), createElementBlock("p", _hoisted_32, " ⚠️ Detection was inferred. Please verify the invoice type is correct. ")) : createCommentVNode("", true)
                ]),
                createBaseVNode("div", _hoisted_33, [
                  _cache[41] || (_cache[41] = createBaseVNode("label", { class: "block text-sm text-gray-700 mb-2" }, "Attach Final Photo", -1)),
                  createBaseVNode("div", {
                    class: normalizeClass(["border-2 border-dashed border-gray-300 rounded-lg p-4 text-center hover:border-blue-400 transition-colors", { "border-blue-400 bg-blue-50": isFinalPhotoDragOver.value }]),
                    onDrop: onFinalPhotoDrop,
                    onDragover: _cache[12] || (_cache[12] = withModifiers(() => {
                    }, ["prevent"])),
                    onDragenter: _cache[13] || (_cache[13] = () => isFinalPhotoDragOver.value = true),
                    onDragleave: onFinalPhotoDragLeave
                  }, [
                    finalize.finalPhotoFile ? (openBlock(), createElementBlock("div", _hoisted_34, [
                      finalPhotoPreviewUrl.value ? (openBlock(), createElementBlock("img", {
                        key: 0,
                        src: finalPhotoPreviewUrl.value,
                        alt: "Final Photo Preview",
                        class: "max-w-full h-auto max-h-32 mx-auto rounded-lg shadow-md"
                      }, null, 8, _hoisted_35)) : createCommentVNode("", true),
                      createBaseVNode("div", { class: "mt-2 flex justify-center space-x-2" }, [
                        createBaseVNode("button", {
                          onClick: clearFinalPhoto,
                          class: "px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded"
                        }, " Remove Photo ")
                      ])
                    ])) : createCommentVNode("", true),
                    !finalize.finalPhotoFile ? (openBlock(), createElementBlock("div", _hoisted_36, [
                      createBaseVNode("div", _hoisted_37, [
                        createBaseVNode("label", _hoisted_38, [
                          createBaseVNode("input", {
                            type: "file",
                            onChange: onFinalPhotoSelected,
                            accept: "image/*",
                            class: "hidden"
                          }, null, 32),
                          _cache[39] || (_cache[39] = createBaseVNode("div", { class: "px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-center text-sm" }, " 📁 Upload Photo ", -1))
                        ]),
                        createBaseVNode("button", {
                          onClick: scanFinalPhoto,
                          disabled: scanning.value,
                          class: "flex-1 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors text-sm"
                        }, [
                          scanning.value ? (openBlock(), createElementBlock("span", _hoisted_40, "🔄 Scanning...")) : (openBlock(), createElementBlock("span", _hoisted_41, "📷 Scan Photo"))
                        ], 8, _hoisted_39)
                      ]),
                      _cache[40] || (_cache[40] = createBaseVNode("div", { class: "text-gray-500 text-xs" }, [
                        createBaseVNode("p", null, "Or drag and drop a photo file here")
                      ], -1))
                    ])) : createCommentVNode("", true)
                  ], 34)
                ]),
                createBaseVNode("div", _hoisted_42, [
                  _cache[42] || (_cache[42] = createBaseVNode("label", { class: "block text-sm text-gray-700 mb-2" }, "Discount (Rs)", -1)),
                  withDirectives(createBaseVNode("input", {
                    type: "number",
                    step: "0.01",
                    class: "w-full px-3 py-2 border rounded",
                    "onUpdate:modelValue": _cache[14] || (_cache[14] = ($event) => invoice.value.totalDiscountAmount = $event)
                  }, null, 512), [
                    [
                      vModelText,
                      invoice.value.totalDiscountAmount,
                      void 0,
                      { number: true }
                    ]
                  ])
                ])
              ]),
              finalize.type === "purchase" ? (openBlock(), createElementBlock("div", _hoisted_43, [
                createBaseVNode("div", _hoisted_44, [
                  _cache[44] || (_cache[44] = createBaseVNode("h3", { class: "font-semibold" }, "Leakages & Bursts (per item)", -1)),
                  deletedRows.value.length > 0 ? (openBlock(), createElementBlock("div", _hoisted_45, [
                    createVNode(_component_Button, {
                      theme: "blue",
                      variant: "outline",
                      size: "sm",
                      onClick: undoLastDelete,
                      class: "hover:bg-blue-50"
                    }, {
                      default: withCtx(() => [
                        _cache[43] || (_cache[43] = createBaseVNode("span", { class: "mr-1 text-blue-600" }, "↶", -1)),
                        createTextVNode(" Undo Delete (" + toDisplayString(deletedRows.value.length) + ") ", 1)
                      ]),
                      _: 1,
                      __: [43]
                    })
                  ])) : createCommentVNode("", true)
                ]),
                itemValidation.value ? (openBlock(), createElementBlock("div", {
                  key: 0,
                  class: normalizeClass(["mb-4 p-3 rounded-md", itemValidation.value.all_valid ? "bg-green-50 border border-green-200" : "bg-yellow-50 border border-yellow-200"])
                }, [
                  createBaseVNode("div", _hoisted_46, [
                    createBaseVNode("div", _hoisted_47, [
                      itemValidation.value.all_valid ? (openBlock(), createElementBlock("div", _hoisted_48, " ✓ ")) : (openBlock(), createElementBlock("div", _hoisted_49, " ⚠ ")),
                      createBaseVNode("div", _hoisted_50, [
                        createBaseVNode("p", {
                          class: normalizeClass(["text-sm font-medium", itemValidation.value.all_valid ? "text-green-800" : "text-yellow-800"])
                        }, toDisplayString(itemValidation.value.all_valid ? "All items are valid" : `${itemValidation.value.missing_items.length} items need to be added to master data`), 3),
                        !itemValidation.value.all_valid ? (openBlock(), createElementBlock("p", _hoisted_51, ' Use the "+" button next to missing items to add them to the master data. After adding items, click "Re-validate Items" to check again. ')) : createCommentVNode("", true)
                      ])
                    ]),
                    createBaseVNode("div", _hoisted_52, [
                      createVNode(_component_Button, {
                        theme: "blue",
                        variant: "outline",
                        size: "sm",
                        onClick: validateItems
                      }, {
                        default: withCtx(() => _cache[45] || (_cache[45] = [
                          createTextVNode(" Re-validate Items ")
                        ])),
                        _: 1,
                        __: [45]
                      }),
                      createVNode(_component_Button, {
                        theme: "gray",
                        variant: "outline",
                        size: "sm",
                        onClick: resetItemStatuses
                      }, {
                        default: withCtx(() => _cache[46] || (_cache[46] = [
                          createTextVNode(" Reset Statuses ")
                        ])),
                        _: 1,
                        __: [46]
                      })
                    ])
                  ])
                ], 2)) : ((_b = (_a = invoice.value) == null ? void 0 : _a.items) == null ? void 0 : _b.length) > 0 ? (openBlock(), createElementBlock("div", _hoisted_53, [
                  createBaseVNode("div", _hoisted_54, [
                    _cache[48] || (_cache[48] = createStaticVNode('<div class="flex items-center" data-v-16a55b67><div class="flex-shrink-0 w-5 h-5 text-gray-400" data-v-16a55b67> ℹ </div><div class="ml-3" data-v-16a55b67><p class="text-sm font-medium text-gray-800" data-v-16a55b67> Validate items before creating invoice </p><p class="text-sm text-gray-600 mt-1" data-v-16a55b67> Click the button to check if all items exist in master data. Validation only runs when you click this button or the &quot;Create Invoice&quot; button. </p></div></div>', 1)),
                    createVNode(_component_Button, {
                      theme: "blue",
                      variant: "outline",
                      size: "sm",
                      onClick: validateItems,
                      class: "ml-4"
                    }, {
                      default: withCtx(() => _cache[47] || (_cache[47] = [
                        createTextVNode(" Validate Items ")
                      ])),
                      _: 1,
                      __: [47]
                    })
                  ])
                ])) : createCommentVNode("", true),
                createBaseVNode("div", _hoisted_55, [
                  createBaseVNode("table", _hoisted_56, [
                    _cache[51] || (_cache[51] = createBaseVNode("thead", { class: "bg-gray-50" }, [
                      createBaseVNode("tr", null, [
                        createBaseVNode("th", { class: "px-2 sm:px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-32 sm:w-48" }, "Code"),
                        createBaseVNode("th", { class: "px-2 sm:px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-48 sm:w-80" }, "Description"),
                        createBaseVNode("th", { class: "px-2 sm:px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-20 sm:w-24" }, "Qty"),
                        createBaseVNode("th", { class: "px-2 sm:px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-20 sm:w-24" }, "UOM"),
                        createBaseVNode("th", { class: "px-2 sm:px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-20 sm:w-24" }, "Leakages"),
                        createBaseVNode("th", { class: "px-2 sm:px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-20 sm:w-24" }, "Bursts"),
                        createBaseVNode("th", { class: "px-2 sm:px-3 py-3 text-center text-xs font-medium text-gray-500 uppercase tracking-wider w-16" }, "Actions")
                      ])
                    ], -1)),
                    createBaseVNode("tbody", _hoisted_57, [
                      (openBlock(true), createElementBlock(Fragment, null, renderList(invoice.value.items, (it, idx) => {
                        return openBlock(), createElementBlock("tr", {
                          key: idx,
                          class: normalizeClass({ "hover:bg-gray-50": true, "bg-red-50": it.isMissing, "bg-green-50": it.itemCreated })
                        }, [
                          createBaseVNode("td", _hoisted_58, [
                            createBaseVNode("div", _hoisted_59, [
                              withDirectives(createBaseVNode("input", {
                                class: normalizeClass(["w-full px-2 sm:px-3 py-2 border rounded text-sm", { "border-red-500": it.isMissing, "border-green-500": it.itemCreated }]),
                                "onUpdate:modelValue": ($event) => it.materialCode = $event,
                                placeholder: "Item Code"
                              }, null, 10, _hoisted_60), [
                                [vModelText, it.materialCode]
                              ]),
                              it.isMissing && !it.itemCreated ? (openBlock(), createElementBlock("button", {
                                key: 0,
                                onClick: ($event) => openNewItemDialog(idx),
                                class: "flex-shrink-0 w-8 h-8 bg-blue-500 hover:bg-blue-600 text-white rounded-full flex items-center justify-center text-lg font-bold transition-colors add-button"
                              }, " + ", 8, _hoisted_61)) : createCommentVNode("", true),
                              it.itemCreated ? (openBlock(), createElementBlock("span", _hoisted_62, " ✓ ")) : createCommentVNode("", true)
                            ])
                          ]),
                          createBaseVNode("td", _hoisted_63, [
                            withDirectives(createBaseVNode("input", {
                              class: "w-full px-2 sm:px-3 py-2 border rounded text-sm",
                              "onUpdate:modelValue": ($event) => it.materialDescription = $event,
                              placeholder: "Description"
                            }, null, 8, _hoisted_64), [
                              [vModelText, it.materialDescription]
                            ])
                          ]),
                          createBaseVNode("td", _hoisted_65, [
                            withDirectives(createBaseVNode("input", {
                              type: "number",
                              class: "w-16 sm:w-20 px-2 sm:px-3 py-2 border rounded text-center",
                              "onUpdate:modelValue": ($event) => it.salesQty = $event,
                              inputmode: "numeric"
                            }, null, 8, _hoisted_66), [
                              [
                                vModelText,
                                it.salesQty,
                                void 0,
                                { number: true }
                              ]
                            ])
                          ]),
                          createBaseVNode("td", _hoisted_67, [
                            withDirectives(createBaseVNode("select", {
                              "onUpdate:modelValue": ($event) => it.uom = $event,
                              class: "px-2 sm:px-3 py-2 border rounded text-center w-16 sm:w-20"
                            }, _cache[49] || (_cache[49] = [
                              createBaseVNode("option", { value: "CS" }, "CS", -1),
                              createBaseVNode("option", { value: "Nos" }, "Nos", -1)
                            ]), 8, _hoisted_68), [
                              [vModelSelect, it.uom]
                            ])
                          ]),
                          createBaseVNode("td", _hoisted_69, [
                            withDirectives(createBaseVNode("input", {
                              type: "number",
                              min: "0",
                              class: "w-16 sm:w-20 px-2 sm:px-3 py-2 border rounded text-center",
                              "onUpdate:modelValue": ($event) => finalize.items[idx].leakages = $event,
                              inputmode: "numeric"
                            }, null, 8, _hoisted_70), [
                              [
                                vModelText,
                                finalize.items[idx].leakages,
                                void 0,
                                { number: true }
                              ]
                            ])
                          ]),
                          createBaseVNode("td", _hoisted_71, [
                            withDirectives(createBaseVNode("input", {
                              type: "number",
                              min: "0",
                              class: "w-16 sm:w-20 px-2 sm:px-3 py-2 border rounded text-center",
                              "onUpdate:modelValue": ($event) => finalize.items[idx].bursts = $event,
                              inputmode: "numeric"
                            }, null, 8, _hoisted_72), [
                              [
                                vModelText,
                                finalize.items[idx].bursts,
                                void 0,
                                { number: true }
                              ]
                            ])
                          ]),
                          createBaseVNode("td", _hoisted_73, [
                            createVNode(_component_Button, {
                              theme: "red",
                              variant: "outline",
                              size: "sm",
                              onClick: ($event) => deleteRow(idx),
                              class: "text-red-600 hover:text-red-700"
                            }, {
                              default: withCtx(() => _cache[50] || (_cache[50] = [
                                createBaseVNode("span", { class: "text-xs" }, "🗑️", -1)
                              ])),
                              _: 2,
                              __: [50]
                            }, 1032, ["onClick"])
                          ])
                        ], 2);
                      }), 128))
                    ])
                  ])
                ])
              ])) : createCommentVNode("", true),
              createBaseVNode("div", _hoisted_74, [
                createVNode(_component_Button, {
                  theme: "green",
                  loading: submitting.value || isProcessing.value,
                  disabled: !finalize.type || isProcessing.value,
                  onClick: confirmAndSubmit
                }, {
                  default: withCtx(() => [
                    createTextVNode(toDisplayString(isProcessing.value ? "Processing..." : `Create ${finalize.type === "purchase" ? "Purchase" : "Sales"} Invoice`), 1)
                  ]),
                  _: 1
                }, 8, ["loading", "disabled"])
              ])
            ])) : createCommentVNode("", true)
          ])
        ]),
        showNewItemDialog.value ? (openBlock(), createElementBlock("div", _hoisted_75, [
          createBaseVNode("div", _hoisted_76, [
            _cache[59] || (_cache[59] = createBaseVNode("div", { class: "px-6 py-4 border-b border-gray-200" }, [
              createBaseVNode("h3", { class: "text-lg font-medium text-gray-900" }, "Create New Item"),
              createBaseVNode("p", { class: "text-sm text-gray-500 mt-1" }, "Add this item to the master data")
            ], -1)),
            createBaseVNode("div", _hoisted_77, [
              createBaseVNode("div", null, [
                _cache[53] || (_cache[53] = createBaseVNode("label", { class: "block text-sm font-medium text-gray-700 mb-1" }, "Item Code *", -1)),
                withDirectives(createBaseVNode("input", {
                  type: "text",
                  "onUpdate:modelValue": _cache[15] || (_cache[15] = ($event) => newItemData.item_code = $event),
                  class: "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                  placeholder: "Enter item code"
                }, null, 512), [
                  [vModelText, newItemData.item_code]
                ])
              ]),
              createBaseVNode("div", null, [
                _cache[54] || (_cache[54] = createBaseVNode("label", { class: "block text-sm font-medium text-gray-700 mb-1" }, "Item Name *", -1)),
                withDirectives(createBaseVNode("input", {
                  type: "text",
                  "onUpdate:modelValue": _cache[16] || (_cache[16] = ($event) => newItemData.item_name = $event),
                  class: "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                  placeholder: "Enter item name"
                }, null, 512), [
                  [vModelText, newItemData.item_name]
                ])
              ]),
              createBaseVNode("div", null, [
                _cache[55] || (_cache[55] = createBaseVNode("label", { class: "block text-sm font-medium text-gray-700 mb-1" }, "Selling Price", -1)),
                withDirectives(createBaseVNode("input", {
                  type: "number",
                  "onUpdate:modelValue": _cache[17] || (_cache[17] = ($event) => newItemData.selling_price = $event),
                  step: "0.01",
                  min: "0",
                  class: "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                  placeholder: "0.00"
                }, null, 512), [
                  [
                    vModelText,
                    newItemData.selling_price,
                    void 0,
                    { number: true }
                  ]
                ])
              ]),
              createBaseVNode("div", null, [
                _cache[56] || (_cache[56] = createBaseVNode("label", { class: "block text-sm font-medium text-gray-700 mb-1" }, "Valuation Price *", -1)),
                withDirectives(createBaseVNode("input", {
                  type: "number",
                  "onUpdate:modelValue": _cache[18] || (_cache[18] = ($event) => newItemData.valuation_price = $event),
                  step: "0.01",
                  min: "0",
                  class: "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500",
                  placeholder: "0.00"
                }, null, 512), [
                  [
                    vModelText,
                    newItemData.valuation_price,
                    void 0,
                    { number: true }
                  ]
                ])
              ]),
              createBaseVNode("div", null, [
                _cache[57] || (_cache[57] = createBaseVNode("label", { class: "block text-sm font-medium text-gray-700 mb-1" }, "Nos in CS (UOM Conversion)", -1)),
                withDirectives(createBaseVNode("input", {
                  type: "number",
                  "onUpdate:modelValue": _cache[19] || (_cache[19] = ($event) => newItemData.uom_conversion = $event),
                  min: "1",
                  step: "1",
                  class: "w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500",
                  placeholder: "6"
                }, null, 512), [
                  [
                    vModelText,
                    newItemData.uom_conversion,
                    void 0,
                    { number: true }
                  ]
                ]),
                _cache[58] || (_cache[58] = createBaseVNode("p", { class: "text-xs text-gray-500 mt-1" }, "How many Nos (pieces) are in 1 CS (Case)", -1))
              ])
            ]),
            createBaseVNode("div", _hoisted_78, [
              createBaseVNode("button", {
                onClick: _cache[20] || (_cache[20] = ($event) => showNewItemDialog.value = false),
                class: "px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
              }, " Cancel "),
              createBaseVNode("button", {
                onClick: createNewItem,
                class: "px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md transition-colors"
              }, " Create Item ")
            ])
          ])
        ])) : createCommentVNode("", true),
        showLastInvoicesDialog.value ? (openBlock(), createElementBlock("div", _hoisted_79, [
          createBaseVNode("div", _hoisted_80, [
            createBaseVNode("div", _hoisted_81, [
              createBaseVNode("h3", _hoisted_82, "Last 3 " + toDisplayString(finalize.type === "purchase" ? "Purchase" : "Sales") + " Invoices", 1),
              _cache[60] || (_cache[60] = createBaseVNode("p", { class: "text-sm text-gray-500 mt-1" }, "Showing the most recent invoices by posting date", -1))
            ]),
            createBaseVNode("div", _hoisted_83, [
              loadingLastInvoices.value ? (openBlock(), createElementBlock("div", _hoisted_84, _cache[61] || (_cache[61] = [
                createBaseVNode("div", { class: "animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" }, null, -1),
                createBaseVNode("span", { class: "ml-3 text-gray-600" }, "Loading invoices...", -1)
              ]))) : lastInvoices.value.length === 0 ? (openBlock(), createElementBlock("div", _hoisted_85, [
                _cache[62] || (_cache[62] = createBaseVNode("div", { class: "text-gray-400 text-6xl mb-4" }, "📄", -1)),
                createBaseVNode("p", _hoisted_86, "No " + toDisplayString(finalize.type === "purchase" ? "purchase" : "sales") + " invoices found", 1)
              ])) : (openBlock(), createElementBlock("div", _hoisted_87, [
                (openBlock(true), createElementBlock(Fragment, null, renderList(lastInvoices.value, (invoice2) => {
                  return openBlock(), createElementBlock("div", {
                    key: invoice2.name,
                    class: "border border-gray-200 rounded-lg p-4 hover:bg-gray-50 transition-colors"
                  }, [
                    createBaseVNode("div", _hoisted_88, [
                      createBaseVNode("div", null, [
                        _cache[63] || (_cache[63] = createBaseVNode("label", { class: "block text-sm font-medium text-gray-700 mb-1" }, "Invoice Name", -1)),
                        createBaseVNode("p", _hoisted_89, toDisplayString(invoice2.name), 1)
                      ]),
                      createBaseVNode("div", null, [
                        _cache[64] || (_cache[64] = createBaseVNode("label", { class: "block text-sm font-medium text-gray-700 mb-1" }, "Posting Date", -1)),
                        createBaseVNode("p", _hoisted_90, toDisplayString(formatDate(invoice2.posting_date)), 1)
                      ]),
                      createBaseVNode("div", null, [
                        _cache[65] || (_cache[65] = createBaseVNode("label", { class: "block text-sm font-medium text-gray-700 mb-1" }, "Amount", -1)),
                        createBaseVNode("p", _hoisted_91, "₹" + toDisplayString(formatAmount(invoice2.grand_total)), 1)
                      ]),
                      createBaseVNode("div", null, [
                        _cache[66] || (_cache[66] = createBaseVNode("label", { class: "block text-sm font-medium text-gray-700 mb-1" }, "Status", -1)),
                        createBaseVNode("span", {
                          class: normalizeClass(["inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium", getStatusClass(invoice2.docstatus)])
                        }, toDisplayString(getStatusText(invoice2.docstatus)), 3)
                      ])
                    ]),
                    finalize.type === "purchase" && invoice2.bill_no ? (openBlock(), createElementBlock("div", _hoisted_92, [
                      createBaseVNode("div", null, [
                        _cache[67] || (_cache[67] = createBaseVNode("label", { class: "block text-xs font-medium text-gray-500 mb-1" }, "Supplier Invoice No", -1)),
                        createBaseVNode("p", _hoisted_93, toDisplayString(invoice2.bill_no), 1)
                      ])
                    ])) : createCommentVNode("", true)
                  ]);
                }), 128))
              ]))
            ]),
            createBaseVNode("div", _hoisted_94, [
              createBaseVNode("button", {
                onClick: _cache[21] || (_cache[21] = ($event) => showLastInvoicesDialog.value = false),
                class: "px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
              }, " Close ")
            ])
          ])
        ])) : createCommentVNode("", true)
      ], 64);
    };
  }
};
const Scanner = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-16a55b67"]]);
export {
  Scanner as default
};
//# sourceMappingURL=Scanner-CwKII1fA.js.map
