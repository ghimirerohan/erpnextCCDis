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
import { s as session } from "./index-DAX_0W7Y.js";
import { m as commonjsGlobal, l as call } from "./ui-C-4uyU25.js";
import { g as ref, o as openBlock, a as createElementBlock, ad as createStaticVNode, b as createBaseVNode, t as toDisplayString, N as withModifiers, n as normalizeClass, e as createCommentVNode, I as createTextVNode, F as Fragment, M as renderList, c as computed, E as normalizeStyle, k as onMounted, L as unref, y as createBlock } from "./vendor-DNPaXrxF.js";
var papaparse_min = { exports: {} };
/* @license
Papa Parse
v5.5.3
https://github.com/mholt/PapaParse
License: MIT
*/
(function(module, exports) {
  ((e, t) => {
    module.exports = t();
  })(commonjsGlobal, function r() {
    var n = "undefined" != typeof self ? self : "undefined" != typeof window ? window : void 0 !== n ? n : {};
    var d, s = !n.document && !!n.postMessage, a = n.IS_PAPA_WORKER || false, o = {}, h = 0, v = {};
    function u(e) {
      this._handle = null, this._finished = false, this._completed = false, this._halted = false, this._input = null, this._baseIndex = 0, this._partialLine = "", this._rowCount = 0, this._start = 0, this._nextChunk = null, this.isFirstChunk = true, this._completeResults = { data: [], errors: [], meta: {} }, function(e2) {
        var t = b(e2);
        t.chunkSize = parseInt(t.chunkSize), e2.step || e2.chunk || (t.chunkSize = null);
        this._handle = new i(t), (this._handle.streamer = this)._config = t;
      }.call(this, e), this.parseChunk = function(t, e2) {
        var i2 = parseInt(this._config.skipFirstNLines) || 0;
        if (this.isFirstChunk && 0 < i2) {
          let e3 = this._config.newline;
          e3 || (r2 = this._config.quoteChar || '"', e3 = this._handle.guessLineEndings(t, r2)), t = [...t.split(e3).slice(i2)].join(e3);
        }
        this.isFirstChunk && U(this._config.beforeFirstChunk) && void 0 !== (r2 = this._config.beforeFirstChunk(t)) && (t = r2), this.isFirstChunk = false, this._halted = false;
        var i2 = this._partialLine + t, r2 = (this._partialLine = "", this._handle.parse(i2, this._baseIndex, !this._finished));
        if (!this._handle.paused() && !this._handle.aborted()) {
          t = r2.meta.cursor, i2 = (this._finished || (this._partialLine = i2.substring(t - this._baseIndex), this._baseIndex = t), r2 && r2.data && (this._rowCount += r2.data.length), this._finished || this._config.preview && this._rowCount >= this._config.preview);
          if (a) n.postMessage({ results: r2, workerId: v.WORKER_ID, finished: i2 });
          else if (U(this._config.chunk) && !e2) {
            if (this._config.chunk(r2, this._handle), this._handle.paused() || this._handle.aborted()) return void (this._halted = true);
            this._completeResults = r2 = void 0;
          }
          return this._config.step || this._config.chunk || (this._completeResults.data = this._completeResults.data.concat(r2.data), this._completeResults.errors = this._completeResults.errors.concat(r2.errors), this._completeResults.meta = r2.meta), this._completed || !i2 || !U(this._config.complete) || r2 && r2.meta.aborted || (this._config.complete(this._completeResults, this._input), this._completed = true), i2 || r2 && r2.meta.paused || this._nextChunk(), r2;
        }
        this._halted = true;
      }, this._sendError = function(e2) {
        U(this._config.error) ? this._config.error(e2) : a && this._config.error && n.postMessage({ workerId: v.WORKER_ID, error: e2, finished: false });
      };
    }
    function f(e) {
      var r2;
      (e = e || {}).chunkSize || (e.chunkSize = v.RemoteChunkSize), u.call(this, e), this._nextChunk = s ? function() {
        this._readChunk(), this._chunkLoaded();
      } : function() {
        this._readChunk();
      }, this.stream = function(e2) {
        this._input = e2, this._nextChunk();
      }, this._readChunk = function() {
        if (this._finished) this._chunkLoaded();
        else {
          if (r2 = new XMLHttpRequest(), this._config.withCredentials && (r2.withCredentials = this._config.withCredentials), s || (r2.onload = y(this._chunkLoaded, this), r2.onerror = y(this._chunkError, this)), r2.open(this._config.downloadRequestBody ? "POST" : "GET", this._input, !s), this._config.downloadRequestHeaders) {
            var e2, t = this._config.downloadRequestHeaders;
            for (e2 in t) r2.setRequestHeader(e2, t[e2]);
          }
          var i2;
          this._config.chunkSize && (i2 = this._start + this._config.chunkSize - 1, r2.setRequestHeader("Range", "bytes=" + this._start + "-" + i2));
          try {
            r2.send(this._config.downloadRequestBody);
          } catch (e3) {
            this._chunkError(e3.message);
          }
          s && 0 === r2.status && this._chunkError();
        }
      }, this._chunkLoaded = function() {
        4 === r2.readyState && (r2.status < 200 || 400 <= r2.status ? this._chunkError() : (this._start += this._config.chunkSize || r2.responseText.length, this._finished = !this._config.chunkSize || this._start >= ((e2) => null !== (e2 = e2.getResponseHeader("Content-Range")) ? parseInt(e2.substring(e2.lastIndexOf("/") + 1)) : -1)(r2), this.parseChunk(r2.responseText)));
      }, this._chunkError = function(e2) {
        e2 = r2.statusText || e2;
        this._sendError(new Error(e2));
      };
    }
    function l(e) {
      (e = e || {}).chunkSize || (e.chunkSize = v.LocalChunkSize), u.call(this, e);
      var i2, r2, n2 = "undefined" != typeof FileReader;
      this.stream = function(e2) {
        this._input = e2, r2 = e2.slice || e2.webkitSlice || e2.mozSlice, n2 ? ((i2 = new FileReader()).onload = y(this._chunkLoaded, this), i2.onerror = y(this._chunkError, this)) : i2 = new FileReaderSync(), this._nextChunk();
      }, this._nextChunk = function() {
        this._finished || this._config.preview && !(this._rowCount < this._config.preview) || this._readChunk();
      }, this._readChunk = function() {
        var e2 = this._input, t = (this._config.chunkSize && (t = Math.min(this._start + this._config.chunkSize, this._input.size), e2 = r2.call(e2, this._start, t)), i2.readAsText(e2, this._config.encoding));
        n2 || this._chunkLoaded({ target: { result: t } });
      }, this._chunkLoaded = function(e2) {
        this._start += this._config.chunkSize, this._finished = !this._config.chunkSize || this._start >= this._input.size, this.parseChunk(e2.target.result);
      }, this._chunkError = function() {
        this._sendError(i2.error);
      };
    }
    function c(e) {
      var i2;
      u.call(this, e = e || {}), this.stream = function(e2) {
        return i2 = e2, this._nextChunk();
      }, this._nextChunk = function() {
        var e2, t;
        if (!this._finished) return e2 = this._config.chunkSize, i2 = e2 ? (t = i2.substring(0, e2), i2.substring(e2)) : (t = i2, ""), this._finished = !i2, this.parseChunk(t);
      };
    }
    function p(e) {
      u.call(this, e = e || {});
      var t = [], i2 = true, r2 = false;
      this.pause = function() {
        u.prototype.pause.apply(this, arguments), this._input.pause();
      }, this.resume = function() {
        u.prototype.resume.apply(this, arguments), this._input.resume();
      }, this.stream = function(e2) {
        this._input = e2, this._input.on("data", this._streamData), this._input.on("end", this._streamEnd), this._input.on("error", this._streamError);
      }, this._checkIsFinished = function() {
        r2 && 1 === t.length && (this._finished = true);
      }, this._nextChunk = function() {
        this._checkIsFinished(), t.length ? this.parseChunk(t.shift()) : i2 = true;
      }, this._streamData = y(function(e2) {
        try {
          t.push("string" == typeof e2 ? e2 : e2.toString(this._config.encoding)), i2 && (i2 = false, this._checkIsFinished(), this.parseChunk(t.shift()));
        } catch (e3) {
          this._streamError(e3);
        }
      }, this), this._streamError = y(function(e2) {
        this._streamCleanUp(), this._sendError(e2);
      }, this), this._streamEnd = y(function() {
        this._streamCleanUp(), r2 = true, this._streamData("");
      }, this), this._streamCleanUp = y(function() {
        this._input.removeListener("data", this._streamData), this._input.removeListener("end", this._streamEnd), this._input.removeListener("error", this._streamError);
      }, this);
    }
    function i(m2) {
      var n2, s2, a2, t, o2 = Math.pow(2, 53), h2 = -o2, u2 = /^\s*-?(\d+\.?|\.\d+|\d+\.\d+)([eE][-+]?\d+)?\s*$/, d2 = /^((\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+([+-][0-2]\d:[0-5]\d|Z))|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d([+-][0-2]\d:[0-5]\d|Z))|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d([+-][0-2]\d:[0-5]\d|Z)))$/, i2 = this, r2 = 0, f2 = 0, l2 = false, e = false, c2 = [], p2 = { data: [], errors: [], meta: {} };
      function y2(e2) {
        return "greedy" === m2.skipEmptyLines ? "" === e2.join("").trim() : 1 === e2.length && 0 === e2[0].length;
      }
      function g2() {
        if (p2 && a2 && (k("Delimiter", "UndetectableDelimiter", "Unable to auto-detect delimiting character; defaulted to '" + v.DefaultDelimiter + "'"), a2 = false), m2.skipEmptyLines && (p2.data = p2.data.filter(function(e3) {
          return !y2(e3);
        })), _2()) {
          let t2 = function(e3, t3) {
            U(m2.transformHeader) && (e3 = m2.transformHeader(e3, t3)), c2.push(e3);
          };
          if (p2) if (Array.isArray(p2.data[0])) {
            for (var e2 = 0; _2() && e2 < p2.data.length; e2++) p2.data[e2].forEach(t2);
            p2.data.splice(0, 1);
          } else p2.data.forEach(t2);
        }
        function i3(e3, t2) {
          for (var i4 = m2.header ? {} : [], r4 = 0; r4 < e3.length; r4++) {
            var n3 = r4, s3 = e3[r4], s3 = ((e4, t3) => ((e5) => (m2.dynamicTypingFunction && void 0 === m2.dynamicTyping[e5] && (m2.dynamicTyping[e5] = m2.dynamicTypingFunction(e5)), true === (m2.dynamicTyping[e5] || m2.dynamicTyping)))(e4) ? "true" === t3 || "TRUE" === t3 || "false" !== t3 && "FALSE" !== t3 && (((e5) => {
              if (u2.test(e5)) {
                e5 = parseFloat(e5);
                if (h2 < e5 && e5 < o2) return 1;
              }
            })(t3) ? parseFloat(t3) : d2.test(t3) ? new Date(t3) : "" === t3 ? null : t3) : t3)(n3 = m2.header ? r4 >= c2.length ? "__parsed_extra" : c2[r4] : n3, s3 = m2.transform ? m2.transform(s3, n3) : s3);
            "__parsed_extra" === n3 ? (i4[n3] = i4[n3] || [], i4[n3].push(s3)) : i4[n3] = s3;
          }
          return m2.header && (r4 > c2.length ? k("FieldMismatch", "TooManyFields", "Too many fields: expected " + c2.length + " fields but parsed " + r4, f2 + t2) : r4 < c2.length && k("FieldMismatch", "TooFewFields", "Too few fields: expected " + c2.length + " fields but parsed " + r4, f2 + t2)), i4;
        }
        var r3;
        p2 && (m2.header || m2.dynamicTyping || m2.transform) && (r3 = 1, !p2.data.length || Array.isArray(p2.data[0]) ? (p2.data = p2.data.map(i3), r3 = p2.data.length) : p2.data = i3(p2.data, 0), m2.header && p2.meta && (p2.meta.fields = c2), f2 += r3);
      }
      function _2() {
        return m2.header && 0 === c2.length;
      }
      function k(e2, t2, i3, r3) {
        e2 = { type: e2, code: t2, message: i3 };
        void 0 !== r3 && (e2.row = r3), p2.errors.push(e2);
      }
      U(m2.step) && (t = m2.step, m2.step = function(e2) {
        p2 = e2, _2() ? g2() : (g2(), 0 !== p2.data.length && (r2 += e2.data.length, m2.preview && r2 > m2.preview ? s2.abort() : (p2.data = p2.data[0], t(p2, i2))));
      }), this.parse = function(e2, t2, i3) {
        var r3 = m2.quoteChar || '"', r3 = (m2.newline || (m2.newline = this.guessLineEndings(e2, r3)), a2 = false, m2.delimiter ? U(m2.delimiter) && (m2.delimiter = m2.delimiter(e2), p2.meta.delimiter = m2.delimiter) : ((r3 = ((e3, t3, i4, r4, n3) => {
          var s3, a3, o3, h3;
          n3 = n3 || [",", "	", "|", ";", v.RECORD_SEP, v.UNIT_SEP];
          for (var u3 = 0; u3 < n3.length; u3++) {
            for (var d3, f3 = n3[u3], l3 = 0, c3 = 0, p3 = 0, g3 = (o3 = void 0, new E({ comments: r4, delimiter: f3, newline: t3, preview: 10 }).parse(e3)), _3 = 0; _3 < g3.data.length; _3++) i4 && y2(g3.data[_3]) ? p3++ : (d3 = g3.data[_3].length, c3 += d3, void 0 === o3 ? o3 = d3 : 0 < d3 && (l3 += Math.abs(d3 - o3), o3 = d3));
            0 < g3.data.length && (c3 /= g3.data.length - p3), (void 0 === a3 || l3 <= a3) && (void 0 === h3 || h3 < c3) && 1.99 < c3 && (a3 = l3, s3 = f3, h3 = c3);
          }
          return { successful: !!(m2.delimiter = s3), bestDelimiter: s3 };
        })(e2, m2.newline, m2.skipEmptyLines, m2.comments, m2.delimitersToGuess)).successful ? m2.delimiter = r3.bestDelimiter : (a2 = true, m2.delimiter = v.DefaultDelimiter), p2.meta.delimiter = m2.delimiter), b(m2));
        return m2.preview && m2.header && r3.preview++, n2 = e2, s2 = new E(r3), p2 = s2.parse(n2, t2, i3), g2(), l2 ? { meta: { paused: true } } : p2 || { meta: { paused: false } };
      }, this.paused = function() {
        return l2;
      }, this.pause = function() {
        l2 = true, s2.abort(), n2 = U(m2.chunk) ? "" : n2.substring(s2.getCharIndex());
      }, this.resume = function() {
        i2.streamer._halted ? (l2 = false, i2.streamer.parseChunk(n2, true)) : setTimeout(i2.resume, 3);
      }, this.aborted = function() {
        return e;
      }, this.abort = function() {
        e = true, s2.abort(), p2.meta.aborted = true, U(m2.complete) && m2.complete(p2), n2 = "";
      }, this.guessLineEndings = function(e2, t2) {
        e2 = e2.substring(0, 1048576);
        var t2 = new RegExp(P(t2) + "([^]*?)" + P(t2), "gm"), i3 = (e2 = e2.replace(t2, "")).split("\r"), t2 = e2.split("\n"), e2 = 1 < t2.length && t2[0].length < i3[0].length;
        if (1 === i3.length || e2) return "\n";
        for (var r3 = 0, n3 = 0; n3 < i3.length; n3++) "\n" === i3[n3][0] && r3++;
        return r3 >= i3.length / 2 ? "\r\n" : "\r";
      };
    }
    function P(e) {
      return e.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    }
    function E(C) {
      var S = (C = C || {}).delimiter, O = C.newline, x = C.comments, I = C.step, A = C.preview, T = C.fastMode, D = null, L = false, F = null == C.quoteChar ? '"' : C.quoteChar, j = F;
      if (void 0 !== C.escapeChar && (j = C.escapeChar), ("string" != typeof S || -1 < v.BAD_DELIMITERS.indexOf(S)) && (S = ","), x === S) throw new Error("Comment character same as delimiter");
      true === x ? x = "#" : ("string" != typeof x || -1 < v.BAD_DELIMITERS.indexOf(x)) && (x = false), "\n" !== O && "\r" !== O && "\r\n" !== O && (O = "\n");
      var z = 0, M = false;
      this.parse = function(i2, t, r2) {
        if ("string" != typeof i2) throw new Error("Input must be a string");
        var n2 = i2.length, e = S.length, s2 = O.length, a2 = x.length, o2 = U(I), h2 = [], u2 = [], d2 = [], f2 = z = 0;
        if (!i2) return w();
        if (T || false !== T && -1 === i2.indexOf(F)) {
          for (var l2 = i2.split(O), c2 = 0; c2 < l2.length; c2++) {
            if (d2 = l2[c2], z += d2.length, c2 !== l2.length - 1) z += O.length;
            else if (r2) return w();
            if (!x || d2.substring(0, a2) !== x) {
              if (o2) {
                if (h2 = [], k(d2.split(S)), R(), M) return w();
              } else k(d2.split(S));
              if (A && A <= c2) return h2 = h2.slice(0, A), w(true);
            }
          }
          return w();
        }
        for (var p2 = i2.indexOf(S, z), g2 = i2.indexOf(O, z), _2 = new RegExp(P(j) + P(F), "g"), m2 = i2.indexOf(F, z); ; ) if (i2[z] === F) for (m2 = z, z++; ; ) {
          if (-1 === (m2 = i2.indexOf(F, m2 + 1))) return r2 || u2.push({ type: "Quotes", code: "MissingQuotes", message: "Quoted field unterminated", row: h2.length, index: z }), E2();
          if (m2 === n2 - 1) return E2(i2.substring(z, m2).replace(_2, F));
          if (F === j && i2[m2 + 1] === j) m2++;
          else if (F === j || 0 === m2 || i2[m2 - 1] !== j) {
            -1 !== p2 && p2 < m2 + 1 && (p2 = i2.indexOf(S, m2 + 1));
            var y2 = v2(-1 === (g2 = -1 !== g2 && g2 < m2 + 1 ? i2.indexOf(O, m2 + 1) : g2) ? p2 : Math.min(p2, g2));
            if (i2.substr(m2 + 1 + y2, e) === S) {
              d2.push(i2.substring(z, m2).replace(_2, F)), i2[z = m2 + 1 + y2 + e] !== F && (m2 = i2.indexOf(F, z)), p2 = i2.indexOf(S, z), g2 = i2.indexOf(O, z);
              break;
            }
            y2 = v2(g2);
            if (i2.substring(m2 + 1 + y2, m2 + 1 + y2 + s2) === O) {
              if (d2.push(i2.substring(z, m2).replace(_2, F)), b2(m2 + 1 + y2 + s2), p2 = i2.indexOf(S, z), m2 = i2.indexOf(F, z), o2 && (R(), M)) return w();
              if (A && h2.length >= A) return w(true);
              break;
            }
            u2.push({ type: "Quotes", code: "InvalidQuotes", message: "Trailing quote on quoted field is malformed", row: h2.length, index: z }), m2++;
          }
        }
        else if (x && 0 === d2.length && i2.substring(z, z + a2) === x) {
          if (-1 === g2) return w();
          z = g2 + s2, g2 = i2.indexOf(O, z), p2 = i2.indexOf(S, z);
        } else if (-1 !== p2 && (p2 < g2 || -1 === g2)) d2.push(i2.substring(z, p2)), z = p2 + e, p2 = i2.indexOf(S, z);
        else {
          if (-1 === g2) break;
          if (d2.push(i2.substring(z, g2)), b2(g2 + s2), o2 && (R(), M)) return w();
          if (A && h2.length >= A) return w(true);
        }
        return E2();
        function k(e2) {
          h2.push(e2), f2 = z;
        }
        function v2(e2) {
          var t2 = 0;
          return t2 = -1 !== e2 && (e2 = i2.substring(m2 + 1, e2)) && "" === e2.trim() ? e2.length : t2;
        }
        function E2(e2) {
          return r2 || (void 0 === e2 && (e2 = i2.substring(z)), d2.push(e2), z = n2, k(d2), o2 && R()), w();
        }
        function b2(e2) {
          z = e2, k(d2), d2 = [], g2 = i2.indexOf(O, z);
        }
        function w(e2) {
          if (C.header && !t && h2.length && !L) {
            var s3 = h2[0], a3 = /* @__PURE__ */ Object.create(null), o3 = new Set(s3);
            let n3 = false;
            for (let r3 = 0; r3 < s3.length; r3++) {
              let i3 = s3[r3];
              if (a3[i3 = U(C.transformHeader) ? C.transformHeader(i3, r3) : i3]) {
                let e3, t2 = a3[i3];
                for (; e3 = i3 + "_" + t2, t2++, o3.has(e3); ) ;
                o3.add(e3), s3[r3] = e3, a3[i3]++, n3 = true, (D = null === D ? {} : D)[e3] = i3;
              } else a3[i3] = 1, s3[r3] = i3;
              o3.add(i3);
            }
            n3 && console.warn("Duplicate headers found and renamed."), L = true;
          }
          return { data: h2, errors: u2, meta: { delimiter: S, linebreak: O, aborted: M, truncated: !!e2, cursor: f2 + (t || 0), renamedHeaders: D } };
        }
        function R() {
          I(w()), h2 = [], u2 = [];
        }
      }, this.abort = function() {
        M = true;
      }, this.getCharIndex = function() {
        return z;
      };
    }
    function g(e) {
      var t = e.data, i2 = o[t.workerId], r2 = false;
      if (t.error) i2.userError(t.error, t.file);
      else if (t.results && t.results.data) {
        var n2 = { abort: function() {
          r2 = true, _(t.workerId, { data: [], errors: [], meta: { aborted: true } });
        }, pause: m, resume: m };
        if (U(i2.userStep)) {
          for (var s2 = 0; s2 < t.results.data.length && (i2.userStep({ data: t.results.data[s2], errors: t.results.errors, meta: t.results.meta }, n2), !r2); s2++) ;
          delete t.results;
        } else U(i2.userChunk) && (i2.userChunk(t.results, n2, t.file), delete t.results);
      }
      t.finished && !r2 && _(t.workerId, t.results);
    }
    function _(e, t) {
      var i2 = o[e];
      U(i2.userComplete) && i2.userComplete(t), i2.terminate(), delete o[e];
    }
    function m() {
      throw new Error("Not implemented.");
    }
    function b(e) {
      if ("object" != typeof e || null === e) return e;
      var t, i2 = Array.isArray(e) ? [] : {};
      for (t in e) i2[t] = b(e[t]);
      return i2;
    }
    function y(e, t) {
      return function() {
        e.apply(t, arguments);
      };
    }
    function U(e) {
      return "function" == typeof e;
    }
    return v.parse = function(e, t) {
      var i2 = (t = t || {}).dynamicTyping || false;
      U(i2) && (t.dynamicTypingFunction = i2, i2 = {});
      if (t.dynamicTyping = i2, t.transform = !!U(t.transform) && t.transform, !t.worker || !v.WORKERS_SUPPORTED) return i2 = null, v.NODE_STREAM_INPUT, "string" == typeof e ? (e = ((e2) => 65279 !== e2.charCodeAt(0) ? e2 : e2.slice(1))(e), i2 = new (t.download ? f : c)(t)) : true === e.readable && U(e.read) && U(e.on) ? i2 = new p(t) : (n.File && e instanceof File || e instanceof Object) && (i2 = new l(t)), i2.stream(e);
      (i2 = (() => {
        var e2;
        return !!v.WORKERS_SUPPORTED && (e2 = (() => {
          var e3 = n.URL || n.webkitURL || null, t2 = r.toString();
          return v.BLOB_URL || (v.BLOB_URL = e3.createObjectURL(new Blob(["var global = (function() { if (typeof self !== 'undefined') { return self; } if (typeof window !== 'undefined') { return window; } if (typeof global !== 'undefined') { return global; } return {}; })(); global.IS_PAPA_WORKER=true; ", "(", t2, ")();"], { type: "text/javascript" })));
        })(), (e2 = new n.Worker(e2)).onmessage = g, e2.id = h++, o[e2.id] = e2);
      })()).userStep = t.step, i2.userChunk = t.chunk, i2.userComplete = t.complete, i2.userError = t.error, t.step = U(t.step), t.chunk = U(t.chunk), t.complete = U(t.complete), t.error = U(t.error), delete t.worker, i2.postMessage({ input: e, config: t, workerId: i2.id });
    }, v.unparse = function(e, t) {
      var n2 = false, _2 = true, m2 = ",", y2 = "\r\n", s2 = '"', a2 = s2 + s2, i2 = false, r2 = null, o2 = false, h2 = ((() => {
        if ("object" == typeof t) {
          if ("string" != typeof t.delimiter || v.BAD_DELIMITERS.filter(function(e2) {
            return -1 !== t.delimiter.indexOf(e2);
          }).length || (m2 = t.delimiter), "boolean" != typeof t.quotes && "function" != typeof t.quotes && !Array.isArray(t.quotes) || (n2 = t.quotes), "boolean" != typeof t.skipEmptyLines && "string" != typeof t.skipEmptyLines || (i2 = t.skipEmptyLines), "string" == typeof t.newline && (y2 = t.newline), "string" == typeof t.quoteChar && (s2 = t.quoteChar), "boolean" == typeof t.header && (_2 = t.header), Array.isArray(t.columns)) {
            if (0 === t.columns.length) throw new Error("Option columns is empty");
            r2 = t.columns;
          }
          void 0 !== t.escapeChar && (a2 = t.escapeChar + s2), t.escapeFormulae instanceof RegExp ? o2 = t.escapeFormulae : "boolean" == typeof t.escapeFormulae && t.escapeFormulae && (o2 = /^[=+\-@\t\r].*$/);
        }
      })(), new RegExp(P(s2), "g"));
      "string" == typeof e && (e = JSON.parse(e));
      if (Array.isArray(e)) {
        if (!e.length || Array.isArray(e[0])) return u2(null, e, i2);
        if ("object" == typeof e[0]) return u2(r2 || Object.keys(e[0]), e, i2);
      } else if ("object" == typeof e) return "string" == typeof e.data && (e.data = JSON.parse(e.data)), Array.isArray(e.data) && (e.fields || (e.fields = e.meta && e.meta.fields || r2), e.fields || (e.fields = Array.isArray(e.data[0]) ? e.fields : "object" == typeof e.data[0] ? Object.keys(e.data[0]) : []), Array.isArray(e.data[0]) || "object" == typeof e.data[0] || (e.data = [e.data])), u2(e.fields || [], e.data || [], i2);
      throw new Error("Unable to serialize unrecognized input");
      function u2(e2, t2, i3) {
        var r3 = "", n3 = ("string" == typeof e2 && (e2 = JSON.parse(e2)), "string" == typeof t2 && (t2 = JSON.parse(t2)), Array.isArray(e2) && 0 < e2.length), s3 = !Array.isArray(t2[0]);
        if (n3 && _2) {
          for (var a3 = 0; a3 < e2.length; a3++) 0 < a3 && (r3 += m2), r3 += k(e2[a3], a3);
          0 < t2.length && (r3 += y2);
        }
        for (var o3 = 0; o3 < t2.length; o3++) {
          var h3 = (n3 ? e2 : t2[o3]).length, u3 = false, d2 = n3 ? 0 === Object.keys(t2[o3]).length : 0 === t2[o3].length;
          if (i3 && !n3 && (u3 = "greedy" === i3 ? "" === t2[o3].join("").trim() : 1 === t2[o3].length && 0 === t2[o3][0].length), "greedy" === i3 && n3) {
            for (var f2 = [], l2 = 0; l2 < h3; l2++) {
              var c2 = s3 ? e2[l2] : l2;
              f2.push(t2[o3][c2]);
            }
            u3 = "" === f2.join("").trim();
          }
          if (!u3) {
            for (var p2 = 0; p2 < h3; p2++) {
              0 < p2 && !d2 && (r3 += m2);
              var g2 = n3 && s3 ? e2[p2] : p2;
              r3 += k(t2[o3][g2], p2);
            }
            o3 < t2.length - 1 && (!i3 || 0 < h3 && !d2) && (r3 += y2);
          }
        }
        return r3;
      }
      function k(e2, t2) {
        var i3, r3;
        return null == e2 ? "" : e2.constructor === Date ? JSON.stringify(e2).slice(1, 25) : (r3 = false, o2 && "string" == typeof e2 && o2.test(e2) && (e2 = "'" + e2, r3 = true), i3 = e2.toString().replace(h2, a2), (r3 = r3 || true === n2 || "function" == typeof n2 && n2(e2, t2) || Array.isArray(n2) && n2[t2] || ((e3, t3) => {
          for (var i4 = 0; i4 < t3.length; i4++) if (-1 < e3.indexOf(t3[i4])) return true;
          return false;
        })(i3, v.BAD_DELIMITERS) || -1 < i3.indexOf(m2) || " " === i3.charAt(0) || " " === i3.charAt(i3.length - 1)) ? s2 + i3 + s2 : i3);
      }
    }, v.RECORD_SEP = String.fromCharCode(30), v.UNIT_SEP = String.fromCharCode(31), v.BYTE_ORDER_MARK = "\uFEFF", v.BAD_DELIMITERS = ["\r", "\n", '"', v.BYTE_ORDER_MARK], v.WORKERS_SUPPORTED = !s && !!n.Worker, v.NODE_STREAM_INPUT = 1, v.LocalChunkSize = 10485760, v.RemoteChunkSize = 5242880, v.DefaultDelimiter = ",", v.Parser = E, v.ParserHandle = i, v.NetworkStreamer = f, v.FileStreamer = l, v.StringStreamer = c, v.ReadableStreamStreamer = p, n.jQuery && ((d = n.jQuery).fn.parse = function(o2) {
      var i2 = o2.config || {}, h2 = [];
      return this.each(function(e2) {
        if (!("INPUT" === d(this).prop("tagName").toUpperCase() && "file" === d(this).attr("type").toLowerCase() && n.FileReader) || !this.files || 0 === this.files.length) return true;
        for (var t = 0; t < this.files.length; t++) h2.push({ file: this.files[t], inputElem: this, instanceConfig: d.extend({}, i2) });
      }), e(), this;
      function e() {
        if (0 === h2.length) U(o2.complete) && o2.complete();
        else {
          var e2, t, i3, r2, n2 = h2[0];
          if (U(o2.before)) {
            var s2 = o2.before(n2.file, n2.inputElem);
            if ("object" == typeof s2) {
              if ("abort" === s2.action) return e2 = "AbortError", t = n2.file, i3 = n2.inputElem, r2 = s2.reason, void (U(o2.error) && o2.error({ name: e2 }, t, i3, r2));
              if ("skip" === s2.action) return void u2();
              "object" == typeof s2.config && (n2.instanceConfig = d.extend(n2.instanceConfig, s2.config));
            } else if ("skip" === s2) return void u2();
          }
          var a2 = n2.instanceConfig.complete;
          n2.instanceConfig.complete = function(e3) {
            U(a2) && a2(e3, n2.file, n2.inputElem), u2();
          }, v.parse(n2.file, n2.instanceConfig);
        }
      }
      function u2() {
        h2.splice(0, 1), e();
      }
    }), a && (n.onmessage = function(e) {
      e = e.data;
      void 0 === v.WORKER_ID && e && (v.WORKER_ID = e.workerId);
      "string" == typeof e.input ? n.postMessage({ workerId: v.WORKER_ID, results: v.parse(e.input, e.config), finished: true }) : (n.File && e.input instanceof File || e.input instanceof Object) && (e = v.parse(e.input, e.config)) && n.postMessage({ workerId: v.WORKER_ID, results: e, finished: true });
    }), (f.prototype = Object.create(u.prototype)).constructor = f, (l.prototype = Object.create(u.prototype)).constructor = l, (c.prototype = Object.create(c.prototype)).constructor = c, (p.prototype = Object.create(u.prototype)).constructor = p, v;
  });
})(papaparse_min);
const _hoisted_1$5 = { class: "bg-white rounded-xl shadow-lg border border-gray-200 p-8" };
const _hoisted_2$5 = { class: "space-y-4" };
const _hoisted_3$5 = { class: "text-lg font-medium text-gray-900" };
const _hoisted_4$5 = {
  key: 0,
  class: "mt-4 p-4 bg-red-50 border border-red-200 rounded-lg"
};
const _hoisted_5$5 = { class: "text-sm text-red-800" };
const _sfc_main$5 = {
  __name: "UploadArea",
  emits: ["file-uploaded"],
  setup(__props, { emit: __emit }) {
    const emit = __emit;
    const fileInput = ref(null);
    const dragOver = ref(false);
    const error = ref(null);
    function triggerFileInput() {
      var _a;
      (_a = fileInput.value) == null ? void 0 : _a.click();
    }
    function handleFileChange(event) {
      var _a;
      const file = (_a = event.target.files) == null ? void 0 : _a[0];
      if (file) {
        validateAndEmitFile(file);
      }
    }
    function handleDrop(event) {
      var _a, _b;
      dragOver.value = false;
      const file = (_b = (_a = event.dataTransfer) == null ? void 0 : _a.files) == null ? void 0 : _b[0];
      if (file) {
        validateAndEmitFile(file);
      }
    }
    function validateAndEmitFile(file) {
      error.value = null;
      if (!file.name.endsWith(".csv")) {
        error.value = "Please upload a CSV file";
        return;
      }
      if (file.size > 10 * 1024 * 1024) {
        error.value = "File size must be less than 10MB";
        return;
      }
      emit("file-uploaded", file);
    }
    return (_ctx, _cache) => {
      return openBlock(), createElementBlock("section", _hoisted_1$5, [
        _cache[5] || (_cache[5] = createStaticVNode('<div class="flex items-center mb-6"><div class="flex items-center justify-center w-10 h-10 bg-indigo-100 rounded-lg mr-3"><svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg></div><h2 class="text-xl font-semibold text-gray-900">Upload CSV File</h2></div>', 1)),
        createBaseVNode("div", {
          onDragover: _cache[0] || (_cache[0] = withModifiers(($event) => dragOver.value = true, ["prevent"])),
          onDragleave: _cache[1] || (_cache[1] = withModifiers(($event) => dragOver.value = false, ["prevent"])),
          onDrop: withModifiers(handleDrop, ["prevent"]),
          onClick: triggerFileInput,
          class: normalizeClass(["relative border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-all duration-200", dragOver.value ? "border-indigo-500 bg-indigo-50" : "border-gray-300 hover:border-indigo-400 hover:bg-gray-50"])
        }, [
          createBaseVNode("input", {
            ref_key: "fileInput",
            ref: fileInput,
            type: "file",
            accept: ".csv",
            onChange: handleFileChange,
            class: "hidden"
          }, null, 544),
          createBaseVNode("div", _hoisted_2$5, [
            _cache[3] || (_cache[3] = createBaseVNode("div", { class: "flex justify-center" }, [
              createBaseVNode("svg", {
                class: "w-16 h-16 text-gray-400",
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
              ])
            ], -1)),
            createBaseVNode("div", null, [
              createBaseVNode("p", _hoisted_3$5, toDisplayString(dragOver.value ? "Drop your CSV file here" : "Drag and drop your CSV file here"), 1),
              _cache[2] || (_cache[2] = createBaseVNode("p", { class: "text-sm text-gray-500 mt-2" }, " or click to browse ", -1))
            ]),
            _cache[4] || (_cache[4] = createBaseVNode("div", { class: "text-xs text-gray-400" }, " Accepted format: CSV file with sales invoice data ", -1))
          ])
        ], 34),
        error.value ? (openBlock(), createElementBlock("div", _hoisted_4$5, [
          createBaseVNode("p", _hoisted_5$5, toDisplayString(error.value), 1)
        ])) : createCommentVNode("", true)
      ]);
    };
  }
};
const _hoisted_1$4 = { class: "bg-white rounded-xl shadow-lg border border-gray-200 p-8" };
const _hoisted_2$4 = { class: "grid grid-cols-1 md:grid-cols-2 gap-6" };
const _hoisted_3$4 = ["value", "disabled"];
const _hoisted_4$4 = { value: "" };
const _hoisted_5$4 = ["value"];
const _hoisted_6$4 = ["value", "disabled"];
const _hoisted_7$4 = { value: "" };
const _hoisted_8$4 = ["value"];
const _sfc_main$4 = {
  __name: "DriverSelect",
  props: {
    driverValue: {
      type: String,
      default: null
    },
    vehicleValue: {
      type: String,
      default: null
    },
    drivers: {
      type: Array,
      default: () => []
    },
    vehicles: {
      type: Array,
      default: () => []
    },
    loadingDrivers: {
      type: Boolean,
      default: false
    },
    loadingVehicles: {
      type: Boolean,
      default: false
    }
  },
  emits: ["update:driverValue", "update:vehicleValue"],
  setup(__props) {
    return (_ctx, _cache) => {
      return openBlock(), createElementBlock("section", _hoisted_1$4, [
        _cache[6] || (_cache[6] = createStaticVNode('<div class="flex items-center mb-6"><div class="flex items-center justify-center w-10 h-10 bg-green-100 rounded-lg mr-3"><svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg></div><h2 class="text-xl font-semibold text-gray-900">Select Driver &amp; Vehicle</h2></div>', 1)),
        createBaseVNode("div", _hoisted_2$4, [
          createBaseVNode("div", null, [
            _cache[2] || (_cache[2] = createBaseVNode("label", { class: "block text-sm font-semibold text-gray-700 mb-3" }, [
              createTextVNode(" Driver "),
              createBaseVNode("span", { class: "text-red-500" }, "*")
            ], -1)),
            createBaseVNode("select", {
              value: __props.driverValue,
              onChange: _cache[0] || (_cache[0] = ($event) => _ctx.$emit("update:driverValue", $event.target.value)),
              class: "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 bg-white",
              disabled: __props.loadingDrivers
            }, [
              createBaseVNode("option", _hoisted_4$4, toDisplayString(__props.loadingDrivers ? "Loading drivers..." : "Select a driver"), 1),
              (openBlock(true), createElementBlock(Fragment, null, renderList(__props.drivers, (driver) => {
                return openBlock(), createElementBlock("option", {
                  key: driver.name,
                  value: driver.name
                }, toDisplayString(driver.employee_name || driver.name), 9, _hoisted_5$4);
              }), 128))
            ], 40, _hoisted_3$4),
            _cache[3] || (_cache[3] = createBaseVNode("p", { class: "mt-2 text-sm text-gray-500" }, " Required: Driver for delivery ", -1))
          ]),
          createBaseVNode("div", null, [
            _cache[4] || (_cache[4] = createBaseVNode("label", { class: "block text-sm font-semibold text-gray-700 mb-3" }, [
              createTextVNode(" Vehicle "),
              createBaseVNode("span", { class: "text-gray-400" }, "(Optional)")
            ], -1)),
            createBaseVNode("select", {
              value: __props.vehicleValue,
              onChange: _cache[1] || (_cache[1] = ($event) => _ctx.$emit("update:vehicleValue", $event.target.value)),
              class: "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all duration-200 bg-white",
              disabled: __props.loadingVehicles
            }, [
              createBaseVNode("option", _hoisted_7$4, toDisplayString(__props.loadingVehicles ? "Loading vehicles..." : "Select a vehicle (optional)"), 1),
              (openBlock(true), createElementBlock(Fragment, null, renderList(__props.vehicles, (vehicle) => {
                return openBlock(), createElementBlock("option", {
                  key: vehicle.name,
                  value: vehicle.name
                }, toDisplayString(vehicle.license_plate ? `${vehicle.name} (${vehicle.license_plate})` : vehicle.name), 9, _hoisted_8$4);
              }), 128))
            ], 40, _hoisted_6$4),
            _cache[5] || (_cache[5] = createBaseVNode("p", { class: "mt-2 text-sm text-gray-500" }, " Optional: Vehicle for delivery ", -1))
          ])
        ])
      ]);
    };
  }
};
const _hoisted_1$3 = { class: "bg-white rounded-xl shadow-lg border border-gray-200 p-8" };
const _hoisted_2$3 = { class: "flex items-center justify-between mb-6" };
const _hoisted_3$3 = { class: "flex items-center" };
const _hoisted_4$3 = { class: "text-sm text-gray-600" };
const _hoisted_5$3 = { class: "overflow-x-auto" };
const _hoisted_6$3 = { class: "min-w-full divide-y divide-gray-200" };
const _hoisted_7$3 = { class: "bg-white divide-y divide-gray-200" };
const _hoisted_8$3 = { class: "px-3 py-4 whitespace-nowrap text-sm text-gray-900" };
const _hoisted_9$3 = { class: "px-3 py-4 whitespace-nowrap text-sm text-gray-900" };
const _hoisted_10$3 = { class: "px-3 py-4 whitespace-nowrap text-sm text-gray-900 font-medium" };
const _hoisted_11$3 = { class: "px-3 py-4 whitespace-nowrap text-sm text-gray-900" };
const _hoisted_12$3 = { class: "px-3 py-4 whitespace-nowrap text-sm text-gray-900" };
const _hoisted_13$3 = { class: "px-3 py-4 whitespace-nowrap text-sm text-gray-900" };
const _hoisted_14$2 = { class: "px-3 py-4 whitespace-nowrap text-sm text-gray-900" };
const _hoisted_15$2 = { class: "px-3 py-4 text-sm text-gray-900" };
const _sfc_main$3 = {
  __name: "PreviewTable",
  props: {
    previewData: {
      type: Array,
      default: () => []
    },
    totalInvoices: {
      type: Number,
      default: 0
    }
  },
  setup(__props) {
    return (_ctx, _cache) => {
      return openBlock(), createElementBlock("section", _hoisted_1$3, [
        createBaseVNode("div", _hoisted_2$3, [
          createBaseVNode("div", _hoisted_3$3, [
            _cache[1] || (_cache[1] = createBaseVNode("div", { class: "flex items-center justify-center w-10 h-10 bg-blue-100 rounded-lg mr-3" }, [
              createBaseVNode("svg", {
                class: "w-5 h-5 text-blue-600",
                fill: "none",
                stroke: "currentColor",
                viewBox: "0 0 24 24"
              }, [
                createBaseVNode("path", {
                  "stroke-linecap": "round",
                  "stroke-linejoin": "round",
                  "stroke-width": "2",
                  d: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
                })
              ])
            ], -1)),
            createBaseVNode("div", null, [
              _cache[0] || (_cache[0] = createBaseVNode("h2", { class: "text-xl font-semibold text-gray-900" }, "Preview", -1)),
              createBaseVNode("p", _hoisted_4$3, "First " + toDisplayString(__props.previewData.length) + " rows • Total " + toDisplayString(__props.totalInvoices) + " invoices", 1)
            ])
          ])
        ]),
        createBaseVNode("div", _hoisted_5$3, [
          createBaseVNode("table", _hoisted_6$3, [
            _cache[2] || (_cache[2] = createBaseVNode("thead", { class: "bg-gray-50" }, [
              createBaseVNode("tr", null, [
                createBaseVNode("th", { class: "px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap" }, "Is Return"),
                createBaseVNode("th", { class: "px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap" }, "Date"),
                createBaseVNode("th", { class: "px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap" }, "Invoice ID"),
                createBaseVNode("th", { class: "px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap" }, "Customer"),
                createBaseVNode("th", { class: "px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap" }, "Item Code"),
                createBaseVNode("th", { class: "px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap" }, "Quantity"),
                createBaseVNode("th", { class: "px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap" }, "Discount"),
                createBaseVNode("th", { class: "px-3 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap" }, "Item Name")
              ])
            ], -1)),
            createBaseVNode("tbody", _hoisted_7$3, [
              (openBlock(true), createElementBlock(Fragment, null, renderList(__props.previewData, (row, index) => {
                return openBlock(), createElementBlock("tr", {
                  key: index,
                  class: normalizeClass(index % 2 === 0 ? "bg-white" : "bg-gray-50")
                }, [
                  createBaseVNode("td", _hoisted_8$3, toDisplayString(row["Is Return (Credit Note)"] || ""), 1),
                  createBaseVNode("td", _hoisted_9$3, toDisplayString(row["Date"] || ""), 1),
                  createBaseVNode("td", _hoisted_10$3, toDisplayString(row["ID"] || ""), 1),
                  createBaseVNode("td", _hoisted_11$3, toDisplayString(row["Customer"] || ""), 1),
                  createBaseVNode("td", _hoisted_12$3, toDisplayString(row["Item (Items)"] || ""), 1),
                  createBaseVNode("td", _hoisted_13$3, toDisplayString(row["Quantity (Items)"] || ""), 1),
                  createBaseVNode("td", _hoisted_14$2, toDisplayString(row["Distributed Discount Amount (Items)"] || ""), 1),
                  createBaseVNode("td", _hoisted_15$2, toDisplayString(row["Item Name (Items)"] || ""), 1)
                ], 2);
              }), 128))
            ])
          ])
        ]),
        _cache[3] || (_cache[3] = createBaseVNode("div", { class: "mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg" }, [
          createBaseVNode("p", { class: "text-sm text-blue-800" }, [
            createBaseVNode("svg", {
              class: "inline w-4 h-4 mr-2",
              fill: "currentColor",
              viewBox: "0 0 20 20"
            }, [
              createBaseVNode("path", {
                "fill-rule": "evenodd",
                d: "M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z",
                "clip-rule": "evenodd"
              })
            ]),
            createTextVNode(" This is a preview of the transformed data. Please review before starting the import. ")
          ])
        ], -1))
      ]);
    };
  }
};
const _hoisted_1$2 = { class: "bg-white rounded-xl shadow-lg border border-gray-200 p-8" };
const _hoisted_2$2 = { class: "mb-6" };
const _hoisted_3$2 = { class: "flex justify-between items-center mb-2" };
const _hoisted_4$2 = { class: "text-sm font-medium text-gray-700" };
const _hoisted_5$2 = { class: "text-sm font-medium text-gray-700" };
const _hoisted_6$2 = { class: "w-full bg-gray-200 rounded-full h-4 overflow-hidden" };
const _hoisted_7$2 = { class: "grid grid-cols-2 md:grid-cols-4 gap-4 mb-6" };
const _hoisted_8$2 = { class: "bg-green-50 border border-green-200 rounded-lg p-4" };
const _hoisted_9$2 = { class: "text-2xl font-bold text-green-600" };
const _hoisted_10$2 = { class: "bg-yellow-50 border border-yellow-200 rounded-lg p-4" };
const _hoisted_11$2 = { class: "text-2xl font-bold text-yellow-600" };
const _hoisted_12$2 = { class: "bg-red-50 border border-red-200 rounded-lg p-4" };
const _hoisted_13$2 = { class: "text-2xl font-bold text-red-600" };
const _hoisted_14$1 = { class: "bg-blue-50 border border-blue-200 rounded-lg p-4" };
const _hoisted_15$1 = { class: "text-2xl font-bold text-blue-600" };
const _hoisted_16$1 = { class: "p-4 bg-gray-50 border border-gray-200 rounded-lg" };
const _hoisted_17$1 = { class: "flex items-start" };
const _hoisted_18$1 = { class: "ml-3 flex-1" };
const _hoisted_19$1 = { class: "text-sm text-gray-600 mt-1" };
const _sfc_main$2 = {
  __name: "ProgressPanel",
  props: {
    progress: {
      type: Object,
      default: () => ({
        processed: 0,
        total: 0,
        message: "",
        imported: 0,
        skipped: 0,
        errors: 0,
        amount: 0
      })
    }
  },
  setup(__props) {
    const props = __props;
    const progressPercent = computed(() => {
      if (props.progress.total === 0) return 0;
      return Math.round(props.progress.processed / props.progress.total * 100);
    });
    function formatAmount(amount) {
      return new Intl.NumberFormat("en-NP", {
        style: "currency",
        currency: "NPR",
        minimumFractionDigits: 2
      }).format(amount);
    }
    return (_ctx, _cache) => {
      return openBlock(), createElementBlock("section", _hoisted_1$2, [
        _cache[6] || (_cache[6] = createStaticVNode('<div class="flex items-center mb-6"><div class="flex items-center justify-center w-10 h-10 bg-yellow-100 rounded-lg mr-3"><svg class="w-5 h-5 text-yellow-600 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg></div><h2 class="text-xl font-semibold text-gray-900">Importing Sales Invoices</h2></div>', 1)),
        createBaseVNode("div", _hoisted_2$2, [
          createBaseVNode("div", _hoisted_3$2, [
            createBaseVNode("span", _hoisted_4$2, " Progress: " + toDisplayString(__props.progress.processed) + " / " + toDisplayString(__props.progress.total), 1),
            createBaseVNode("span", _hoisted_5$2, toDisplayString(progressPercent.value) + "% ", 1)
          ]),
          createBaseVNode("div", _hoisted_6$2, [
            createBaseVNode("div", {
              class: "bg-indigo-600 h-4 rounded-full transition-all duration-300 ease-out",
              style: normalizeStyle({ width: progressPercent.value + "%" })
            }, null, 4)
          ])
        ]),
        createBaseVNode("div", _hoisted_7$2, [
          createBaseVNode("div", _hoisted_8$2, [
            createBaseVNode("div", _hoisted_9$2, toDisplayString(__props.progress.imported), 1),
            _cache[0] || (_cache[0] = createBaseVNode("div", { class: "text-sm text-green-700" }, "Imported", -1))
          ]),
          createBaseVNode("div", _hoisted_10$2, [
            createBaseVNode("div", _hoisted_11$2, toDisplayString(__props.progress.skipped), 1),
            _cache[1] || (_cache[1] = createBaseVNode("div", { class: "text-sm text-yellow-700" }, "Skipped", -1))
          ]),
          createBaseVNode("div", _hoisted_12$2, [
            createBaseVNode("div", _hoisted_13$2, toDisplayString(__props.progress.errors), 1),
            _cache[2] || (_cache[2] = createBaseVNode("div", { class: "text-sm text-red-700" }, "Errors", -1))
          ]),
          createBaseVNode("div", _hoisted_14$1, [
            createBaseVNode("div", _hoisted_15$1, toDisplayString(formatAmount(__props.progress.amount)), 1),
            _cache[3] || (_cache[3] = createBaseVNode("div", { class: "text-sm text-blue-700" }, "Total Amount", -1))
          ])
        ]),
        createBaseVNode("div", _hoisted_16$1, [
          createBaseVNode("div", _hoisted_17$1, [
            _cache[5] || (_cache[5] = createBaseVNode("div", { class: "flex-shrink-0" }, [
              createBaseVNode("svg", {
                class: "w-5 h-5 text-gray-400 mt-0.5",
                fill: "currentColor",
                viewBox: "0 0 20 20"
              }, [
                createBaseVNode("path", {
                  "fill-rule": "evenodd",
                  d: "M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z",
                  "clip-rule": "evenodd"
                })
              ])
            ], -1)),
            createBaseVNode("div", _hoisted_18$1, [
              _cache[4] || (_cache[4] = createBaseVNode("p", { class: "text-sm font-medium text-gray-900" }, "Current Status", -1)),
              createBaseVNode("p", _hoisted_19$1, toDisplayString(__props.progress.message || "Processing..."), 1)
            ])
          ])
        ])
      ]);
    };
  }
};
const _hoisted_1$1 = { class: "bg-white rounded-xl shadow-lg border border-gray-200 p-8" };
const _hoisted_2$1 = { class: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6" };
const _hoisted_3$1 = { class: "bg-gray-50 border border-gray-200 rounded-lg p-6" };
const _hoisted_4$1 = { class: "text-3xl font-bold text-gray-900" };
const _hoisted_5$1 = { class: "bg-green-50 border border-green-200 rounded-lg p-6" };
const _hoisted_6$1 = { class: "text-3xl font-bold text-green-600" };
const _hoisted_7$1 = { class: "bg-yellow-50 border border-yellow-200 rounded-lg p-6" };
const _hoisted_8$1 = { class: "text-3xl font-bold text-yellow-600" };
const _hoisted_9$1 = { class: "bg-red-50 border border-red-200 rounded-lg p-6" };
const _hoisted_10$1 = { class: "text-3xl font-bold text-red-600" };
const _hoisted_11$1 = { class: "bg-gradient-to-r from-indigo-50 to-blue-50 border border-indigo-200 rounded-lg p-6 mb-6" };
const _hoisted_12$1 = { class: "flex items-center justify-between" };
const _hoisted_13$1 = { class: "text-3xl font-bold text-indigo-900 mt-2" };
const _hoisted_14 = { class: "flex flex-col sm:flex-row gap-4" };
const _hoisted_15 = ["href"];
const _hoisted_16 = {
  key: 0,
  class: "mt-6 p-4 bg-green-50 border border-green-200 rounded-lg"
};
const _hoisted_17 = { class: "flex" };
const _hoisted_18 = { class: "ml-3" };
const _hoisted_19 = { class: "text-sm font-medium text-green-800" };
const _hoisted_20 = {
  key: 1,
  class: "mt-6 p-4 bg-red-50 border border-red-200 rounded-lg"
};
const _hoisted_21 = { class: "flex" };
const _hoisted_22 = { class: "ml-3" };
const _hoisted_23 = { class: "text-sm font-medium text-red-800" };
const _sfc_main$1 = {
  __name: "SummaryCard",
  props: {
    summary: {
      type: Object,
      default: () => ({
        total: 0,
        imported: 0,
        skipped: 0,
        errors: 0,
        amount: 0,
        errorCsvPath: null
      })
    }
  },
  emits: ["start-new"],
  setup(__props) {
    function formatAmount(amount) {
      return new Intl.NumberFormat("en-NP", {
        style: "currency",
        currency: "NPR",
        minimumFractionDigits: 2
      }).format(amount);
    }
    return (_ctx, _cache) => {
      return openBlock(), createElementBlock("section", _hoisted_1$1, [
        _cache[13] || (_cache[13] = createStaticVNode('<div class="flex items-center mb-6"><div class="flex items-center justify-center w-10 h-10 bg-green-100 rounded-lg mr-3"><svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg></div><h2 class="text-xl font-semibold text-gray-900">Import Complete</h2></div>', 1)),
        createBaseVNode("div", _hoisted_2$1, [
          createBaseVNode("div", _hoisted_3$1, [
            createBaseVNode("div", _hoisted_4$1, toDisplayString(__props.summary.total), 1),
            _cache[1] || (_cache[1] = createBaseVNode("div", { class: "text-sm text-gray-600 mt-1" }, "Total Invoices", -1))
          ]),
          createBaseVNode("div", _hoisted_5$1, [
            createBaseVNode("div", _hoisted_6$1, toDisplayString(__props.summary.imported), 1),
            _cache[2] || (_cache[2] = createBaseVNode("div", { class: "text-sm text-green-700 mt-1" }, "Successfully Imported", -1))
          ]),
          createBaseVNode("div", _hoisted_7$1, [
            createBaseVNode("div", _hoisted_8$1, toDisplayString(__props.summary.skipped), 1),
            _cache[3] || (_cache[3] = createBaseVNode("div", { class: "text-sm text-yellow-700 mt-1" }, "Skipped (Already Exist)", -1))
          ]),
          createBaseVNode("div", _hoisted_9$1, [
            createBaseVNode("div", _hoisted_10$1, toDisplayString(__props.summary.errors), 1),
            _cache[4] || (_cache[4] = createBaseVNode("div", { class: "text-sm text-red-700 mt-1" }, "Errors", -1))
          ])
        ]),
        createBaseVNode("div", _hoisted_11$1, [
          createBaseVNode("div", _hoisted_12$1, [
            createBaseVNode("div", null, [
              _cache[5] || (_cache[5] = createBaseVNode("div", { class: "text-sm text-indigo-700 font-medium" }, "Total Amount Imported", -1)),
              createBaseVNode("div", _hoisted_13$1, toDisplayString(formatAmount(__props.summary.amount)), 1)
            ]),
            _cache[6] || (_cache[6] = createBaseVNode("div", { class: "flex items-center justify-center w-16 h-16 bg-indigo-100 rounded-full" }, [
              createBaseVNode("svg", {
                class: "w-8 h-8 text-indigo-600",
                fill: "none",
                stroke: "currentColor",
                viewBox: "0 0 24 24"
              }, [
                createBaseVNode("path", {
                  "stroke-linecap": "round",
                  "stroke-linejoin": "round",
                  "stroke-width": "2",
                  d: "M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                })
              ])
            ], -1))
          ])
        ]),
        createBaseVNode("div", _hoisted_14, [
          createBaseVNode("button", {
            onClick: _cache[0] || (_cache[0] = ($event) => _ctx.$emit("start-new")),
            class: "flex-1 inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-lg shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors duration-200"
          }, _cache[7] || (_cache[7] = [
            createBaseVNode("svg", {
              class: "w-5 h-5 mr-2",
              fill: "none",
              stroke: "currentColor",
              viewBox: "0 0 24 24"
            }, [
              createBaseVNode("path", {
                "stroke-linecap": "round",
                "stroke-linejoin": "round",
                "stroke-width": "2",
                d: "M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
              })
            ], -1),
            createTextVNode(" Upload Another File ")
          ])),
          __props.summary.errors > 0 && __props.summary.errorCsvPath ? (openBlock(), createElementBlock("a", {
            key: 0,
            href: __props.summary.errorCsvPath,
            download: "",
            class: "flex-1 inline-flex items-center justify-center px-6 py-3 border border-red-300 text-base font-medium rounded-lg shadow-sm text-red-700 bg-white hover:bg-red-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-colors duration-200"
          }, _cache[8] || (_cache[8] = [
            createBaseVNode("svg", {
              class: "w-5 h-5 mr-2",
              fill: "none",
              stroke: "currentColor",
              viewBox: "0 0 24 24"
            }, [
              createBaseVNode("path", {
                "stroke-linecap": "round",
                "stroke-linejoin": "round",
                "stroke-width": "2",
                d: "M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              })
            ], -1),
            createTextVNode(" Download Error CSV ")
          ]), 8, _hoisted_15)) : createCommentVNode("", true)
        ]),
        __props.summary.imported > 0 ? (openBlock(), createElementBlock("div", _hoisted_16, [
          createBaseVNode("div", _hoisted_17, [
            _cache[10] || (_cache[10] = createBaseVNode("div", { class: "flex-shrink-0" }, [
              createBaseVNode("svg", {
                class: "w-5 h-5 text-green-400",
                fill: "currentColor",
                viewBox: "0 0 20 20"
              }, [
                createBaseVNode("path", {
                  "fill-rule": "evenodd",
                  d: "M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z",
                  "clip-rule": "evenodd"
                })
              ])
            ], -1)),
            createBaseVNode("div", _hoisted_18, [
              createBaseVNode("p", _hoisted_19, " Successfully imported " + toDisplayString(__props.summary.imported) + " sales invoice" + toDisplayString(__props.summary.imported !== 1 ? "s" : "") + "! ", 1),
              _cache[9] || (_cache[9] = createBaseVNode("p", { class: "text-sm text-green-700 mt-1" }, " All invoices are in draft status. You can review and submit them from the Sales Invoice list. ", -1))
            ])
          ])
        ])) : createCommentVNode("", true),
        __props.summary.errors > 0 ? (openBlock(), createElementBlock("div", _hoisted_20, [
          createBaseVNode("div", _hoisted_21, [
            _cache[12] || (_cache[12] = createBaseVNode("div", { class: "flex-shrink-0" }, [
              createBaseVNode("svg", {
                class: "w-5 h-5 text-red-400",
                fill: "currentColor",
                viewBox: "0 0 20 20"
              }, [
                createBaseVNode("path", {
                  "fill-rule": "evenodd",
                  d: "M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z",
                  "clip-rule": "evenodd"
                })
              ])
            ], -1)),
            createBaseVNode("div", _hoisted_22, [
              createBaseVNode("p", _hoisted_23, toDisplayString(__props.summary.errors) + " invoice" + toDisplayString(__props.summary.errors !== 1 ? "s" : "") + " failed to import ", 1),
              _cache[11] || (_cache[11] = createBaseVNode("p", { class: "text-sm text-red-700 mt-1" }, " Download the error CSV to see details and fix the issues. ", -1))
            ])
          ])
        ])) : createCommentVNode("", true)
      ]);
    };
  }
};
const _hoisted_1 = { class: "min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50" };
const _hoisted_2 = { class: "bg-white shadow-sm border-b border-gray-200 sticky top-0 z-20" };
const _hoisted_3 = { class: "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8" };
const _hoisted_4 = { class: "flex justify-between items-center py-6" };
const _hoisted_5 = { class: "flex items-center space-x-4" };
const _hoisted_6 = { class: "text-sm text-gray-600" };
const _hoisted_7 = { class: "max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8" };
const _hoisted_8 = {
  key: 1,
  class: "bg-white rounded-xl shadow-lg border border-gray-200 p-6"
};
const _hoisted_9 = { class: "flex items-center justify-between" };
const _hoisted_10 = { class: "flex items-center space-x-3" };
const _hoisted_11 = { class: "text-sm text-gray-500" };
const _hoisted_12 = {
  key: 4,
  class: "flex justify-center"
};
const _hoisted_13 = ["disabled"];
const _sfc_main = {
  __name: "UploadSales",
  setup(__props) {
    const csvContent = ref(null);
    const selectedDriver = ref(null);
    const selectedVehicle = ref(null);
    const drivers = ref([]);
    const vehicles = ref([]);
    const loadingDrivers = ref(false);
    const loadingVehicles = ref(false);
    const previewData = ref([]);
    const totalInvoices = ref(0);
    const importing = ref(false);
    const showProgress = ref(false);
    const showSummary = ref(false);
    const progress = ref({
      processed: 0,
      total: 0,
      message: "",
      imported: 0,
      skipped: 0,
      errors: 0,
      amount: 0
    });
    const summary = ref(null);
    onMounted(() => __async(this, null, function* () {
      yield Promise.all([loadDrivers(), loadVehicles()]);
    }));
    function loadDrivers() {
      return __async(this, null, function* () {
        loadingDrivers.value = true;
        try {
          const response = yield call("custom_erp.custom_erp.api.uploadsales.get_drivers");
          if (response.success) {
            drivers.value = response.drivers;
          }
        } catch (error) {
          console.error("Error loading drivers:", error);
        } finally {
          loadingDrivers.value = false;
        }
      });
    }
    function loadVehicles() {
      return __async(this, null, function* () {
        loadingVehicles.value = true;
        try {
          const response = yield call("custom_erp.custom_erp.api.uploadsales.get_vehicles");
          if (response.success) {
            vehicles.value = response.vehicles;
          }
        } catch (error) {
          console.error("Error loading vehicles:", error);
        } finally {
          loadingVehicles.value = false;
        }
      });
    }
    function handleFileUpload(file) {
      return __async(this, null, function* () {
        try {
          const text = yield file.text();
          csvContent.value = text;
          const response = yield call("custom_erp.custom_erp.api.uploadsales.transform_and_preview", {
            csv_content: text
          });
          if (response.success) {
            previewData.value = response.preview_rows || [];
            totalInvoices.value = response.total_invoices || 0;
          } else {
            alert("Error generating preview: " + (response.error || "Unknown error"));
          }
        } catch (error) {
          console.error("Error handling file upload:", error);
          alert("Error processing file: " + error.message);
        }
      });
    }
    function clearFile() {
      if (confirm("Clear current file and selections?")) {
        csvContent.value = null;
        selectedDriver.value = null;
        selectedVehicle.value = null;
        previewData.value = [];
        totalInvoices.value = 0;
      }
    }
    function startImport() {
      return __async(this, null, function* () {
        if (!selectedDriver.value) {
          alert("Please select a driver");
          return;
        }
        let confirmMsg = `Import ${totalInvoices.value} invoices with driver ${selectedDriver.value}`;
        if (selectedVehicle.value) {
          confirmMsg += ` and vehicle ${selectedVehicle.value}`;
        }
        confirmMsg += "?";
        if (!confirm(confirmMsg)) {
          return;
        }
        importing.value = true;
        showProgress.value = true;
        try {
          const response = yield call("custom_erp.custom_erp.api.uploadsales.enqueue_import_job", {
            driver_id: selectedDriver.value,
            vehicle_id: selectedVehicle.value || "",
            csv_content: csvContent.value
          });
          if (response.success) {
            subscribeToProgress();
          } else {
            alert("Error starting import: " + (response.error || "Unknown error"));
            showProgress.value = false;
          }
        } catch (error) {
          console.error("Error starting import:", error);
          alert("Error starting import: " + error.message);
          showProgress.value = false;
        } finally {
          importing.value = false;
        }
      });
    }
    function subscribeToProgress() {
      if (!window.frappe || !window.frappe.realtime) {
        console.error("Frappe realtime not available");
        return;
      }
      window.frappe.realtime.on("uploadsales_progress", (data) => {
        progress.value = {
          processed: data.processed || 0,
          total: data.total || 0,
          message: data.current_message || "",
          imported: data.imported_count || 0,
          skipped: data.skipped_count || 0,
          errors: data.error_count || 0,
          amount: data.total_amount || 0
        };
        if (data.completed) {
          showProgress.value = false;
          showSummary.value = true;
          summary.value = {
            total: data.total || 0,
            imported: data.imported_count || 0,
            skipped: data.skipped_count || 0,
            errors: data.error_count || 0,
            amount: data.total_amount || 0,
            errorCsvPath: data.error_csv_path || null
          };
          window.frappe.realtime.off("uploadsales_progress");
        }
      });
    }
    function resetUpload() {
      csvContent.value = null;
      selectedDriver.value = null;
      selectedVehicle.value = null;
      previewData.value = [];
      totalInvoices.value = 0;
      importing.value = false;
      showProgress.value = false;
      showSummary.value = false;
      progress.value = {
        processed: 0,
        total: 0,
        message: "",
        imported: 0,
        skipped: 0,
        errors: 0,
        amount: 0
      };
      summary.value = null;
    }
    return (_ctx, _cache) => {
      return openBlock(), createElementBlock("div", _hoisted_1, [
        createBaseVNode("header", _hoisted_2, [
          createBaseVNode("div", _hoisted_3, [
            createBaseVNode("div", _hoisted_4, [
              createBaseVNode("div", _hoisted_5, [
                _cache[4] || (_cache[4] = createBaseVNode("div", { class: "flex items-center justify-center w-12 h-12 bg-indigo-600 rounded-lg" }, [
                  createBaseVNode("svg", {
                    class: "w-6 h-6 text-white",
                    fill: "none",
                    stroke: "currentColor",
                    viewBox: "0 0 24 24"
                  }, [
                    createBaseVNode("path", {
                      "stroke-linecap": "round",
                      "stroke-linejoin": "round",
                      "stroke-width": "2",
                      d: "M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                    })
                  ])
                ], -1)),
                createBaseVNode("div", null, [
                  _cache[3] || (_cache[3] = createBaseVNode("h1", { class: "text-2xl font-bold text-gray-900" }, "Upload Sales Invoices", -1)),
                  createBaseVNode("p", _hoisted_6, "Bulk import sales invoices from CSV • " + toDisplayString(unref(session).user), 1)
                ])
              ]),
              createBaseVNode("button", {
                onClick: _cache[0] || (_cache[0] = ($event) => unref(session).logout.submit()),
                class: "inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              }, _cache[5] || (_cache[5] = [
                createBaseVNode("svg", {
                  class: "w-4 h-4 mr-2",
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
                createTextVNode(" Logout ")
              ]))
            ])
          ])
        ]),
        createBaseVNode("main", _hoisted_7, [
          !csvContent.value && !showProgress.value && !showSummary.value ? (openBlock(), createBlock(_sfc_main$5, {
            key: 0,
            onFileUploaded: handleFileUpload
          })) : createCommentVNode("", true),
          csvContent.value && !showProgress.value && !showSummary.value ? (openBlock(), createElementBlock("div", _hoisted_8, [
            createBaseVNode("div", _hoisted_9, [
              createBaseVNode("div", _hoisted_10, [
                _cache[7] || (_cache[7] = createBaseVNode("div", { class: "flex items-center justify-center w-10 h-10 bg-blue-100 rounded-lg" }, [
                  createBaseVNode("svg", {
                    class: "w-5 h-5 text-blue-600",
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
                  ])
                ], -1)),
                createBaseVNode("div", null, [
                  _cache[6] || (_cache[6] = createBaseVNode("p", { class: "text-sm font-medium text-gray-900" }, "CSV file loaded", -1)),
                  createBaseVNode("p", _hoisted_11, "Ready to import " + toDisplayString(totalInvoices.value) + " invoices", 1)
                ])
              ]),
              createBaseVNode("button", {
                onClick: clearFile,
                class: "inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              }, _cache[8] || (_cache[8] = [
                createBaseVNode("svg", {
                  class: "w-4 h-4 mr-2",
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
                ], -1),
                createTextVNode(" Clear File ")
              ]))
            ])
          ])) : createCommentVNode("", true),
          csvContent.value && !showProgress.value && !showSummary.value ? (openBlock(), createBlock(_sfc_main$4, {
            key: 2,
            driverValue: selectedDriver.value,
            "onUpdate:driverValue": _cache[1] || (_cache[1] = ($event) => selectedDriver.value = $event),
            vehicleValue: selectedVehicle.value,
            "onUpdate:vehicleValue": _cache[2] || (_cache[2] = ($event) => selectedVehicle.value = $event),
            drivers: drivers.value,
            vehicles: vehicles.value,
            "loading-drivers": loadingDrivers.value,
            "loading-vehicles": loadingVehicles.value
          }, null, 8, ["driverValue", "vehicleValue", "drivers", "vehicles", "loading-drivers", "loading-vehicles"])) : createCommentVNode("", true),
          previewData.value.length > 0 && !showProgress.value && !showSummary.value ? (openBlock(), createBlock(_sfc_main$3, {
            key: 3,
            "preview-data": previewData.value,
            "total-invoices": totalInvoices.value
          }, null, 8, ["preview-data", "total-invoices"])) : createCommentVNode("", true),
          csvContent.value && !showProgress.value && !showSummary.value ? (openBlock(), createElementBlock("div", _hoisted_12, [
            createBaseVNode("button", {
              onClick: startImport,
              disabled: !selectedDriver.value || importing.value,
              class: "inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-lg shadow-lg text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
            }, [
              _cache[9] || (_cache[9] = createBaseVNode("svg", {
                class: "w-6 h-6 mr-3",
                fill: "none",
                stroke: "currentColor",
                viewBox: "0 0 24 24"
              }, [
                createBaseVNode("path", {
                  "stroke-linecap": "round",
                  "stroke-linejoin": "round",
                  "stroke-width": "2",
                  d: "M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                })
              ], -1)),
              createTextVNode(" " + toDisplayString(selectedDriver.value ? "Start Import" : "Please select a driver first"), 1)
            ], 8, _hoisted_13)
          ])) : createCommentVNode("", true),
          showProgress.value ? (openBlock(), createBlock(_sfc_main$2, {
            key: 5,
            progress: progress.value
          }, null, 8, ["progress"])) : createCommentVNode("", true),
          showSummary.value ? (openBlock(), createBlock(_sfc_main$1, {
            key: 6,
            summary: summary.value,
            onStartNew: resetUpload
          }, null, 8, ["summary"])) : createCommentVNode("", true)
        ])
      ]);
    };
  }
};
export {
  _sfc_main as default
};
//# sourceMappingURL=UploadSales-CAlKfAmr.js.map
