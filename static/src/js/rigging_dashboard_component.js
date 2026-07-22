/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

function selectionMatches(labelsMap, query) {
    const q = query.toLowerCase();
    return Object.entries(labelsMap)
        .filter(([, label]) => label.toLowerCase().includes(q))
        .map(([value]) => value);
}

function orDomain(conditions) {
    if (!conditions.length) return [];
    if (conditions.length === 1) return [conditions[0]];
    const pipes = Array(conditions.length - 1).fill("|");
    return [...pipes, ...conditions];
}

const TABS = [
    { key: "rigs",       label: "Rigs" },
    { key: "components", label: "Components" },
    { key: "rigging",    label: "Rigging" },
    { key: "schedule",   label: "Schedule" },
];

const CONFIG = {
    rigs: {
        model: "rigging.rig",
        fields: ["number", "owner_id", "usage_type", "canopy_id", "container_id", "reserve_id", "aad_id"],
        columns: [
            { field: "number",       label: "Rig #" },
            { field: "owner_id",     label: "Owner" },
            { field: "usage_type",   label: "Type" },
            { field: "canopy_id",    label: "Canopy" },
            { field: "container_id", label: "Container" },
            { field: "reserve_id",   label: "Reserve" },
            { field: "aad_id",       label: "AAD" },
        ],
        searchDomain: (q) => {
            const conds = [
                ["number",            "ilike", q],
                ["owner_id.name",     "ilike", q],
                ["canopy_id.name",    "ilike", q],
                ["container_id.name", "ilike", q],
                ["reserve_id.name",   "ilike", q],
                ["aad_id.name",       "ilike", q],
            ];
            selectionMatches(LABELS.usage_type, q).forEach(v => conds.push(["usage_type", "=", v]));
            return orDomain(conds);
        },
        order: "number asc",
    },
    components: {
        model: "rigging.component",
        fields: ["name", "component_type", "usage_type", "model_id", "size_id", "owner_id", "rig_id", "is_mounted"],
        columns: [
            { field: "name",           label: "Serial" },
            { field: "component_type", label: "Type" },
            { field: "usage_type",     label: "Discipline" },
            { field: "model_id",       label: "Model" },
            { field: "size_id",        label: "Size" },
            { field: "owner_id",       label: "Owner" },
            { field: "rig_id",         label: "Rig" },
            { field: "is_mounted",     label: "Mounted" },
        ],
        searchDomain: (q) => {
            const conds = [
                ["name",          "ilike", q],
                ["owner_id.name", "ilike", q],
                ["model_id.name", "ilike", q],
                ["size_id.name",  "ilike", q],
                ["rig_id.number", "ilike", q],
            ];
            selectionMatches(LABELS.component_type, q).forEach(v => conds.push(["component_type", "=", v]));
            selectionMatches(LABELS.usage_type,     q).forEach(v => conds.push(["usage_type",     "=", v]));
            return orDomain(conds);
        },
        order: "name asc",
    },
    rigging: {
        model: "rigging.rigging",
        fields: ["name", "date", "component_id", "owner_id", "rigging_type", "state", "price"],
        columns: [
            { field: "name",         label: "Reference" },
            { field: "date",         label: "Date" },
            { field: "component_id", label: "Component" },
            { field: "owner_id",     label: "Owner" },
            { field: "rigging_type", label: "Type" },
            { field: "state",        label: "State" },
            { field: "price",        label: "Price" },
        ],
        searchDomain: (q) => {
            const conds = [
                ["name",              "ilike", q],
                ["owner_id.name",     "ilike", q],
                ["component_id.name", "ilike", q],
            ];
            selectionMatches(LABELS.rigging_type, q).forEach(v => conds.push(["rigging_type", "=", v]));
            selectionMatches(LABELS.state,        q).forEach(v => conds.push(["state",        "=", v]));
            return orDomain(conds);
        },
        order: "date desc",
    },
};

const LABELS = {
    usage_type:   { sport: "Sport", tandem: "Tandem", pilot: "Pilot" },
    component_type: { canopy: "Canopy", container: "Container", reserve: "Reserve", aad: "AAD" },
    rigging_type: { inspection_repack: "I + R", repair: "Repair", alteration: "Alteration", fabrication: "Fabrication" },
    state:        { pending: "Pending", paid: "Paid" },
};

export class RiggingDashboard extends Component {
    static template = "rigging.RiggingDashboard";

    setup() {
        this.orm  = useService("orm");
        this.tabs = TABS;
        this.state = useState({
            activeTab:   "rigs",
            records:     [],
            searchQuery: "",
            loading:     false,
        });
        onWillStart(() => this._load());
    }

    get columns() {
        return CONFIG[this.state.activeTab]?.columns || [];
    }

    async _load() {
        const { activeTab, searchQuery } = this.state;
        const cfg = CONFIG[activeTab];
        if (!cfg) { this.state.records = []; return; }
        this.state.loading = true;
        const domain = searchQuery ? cfg.searchDomain(searchQuery) : [];
        this.state.records = await this.orm.searchRead(
            cfg.model, domain, cfg.fields,
            { limit: 100, order: cfg.order }
        );
        this.state.loading = false;
    }

    async setTab(tab) {
        this.state.activeTab   = tab;
        this.state.searchQuery = "";
        this.state.records     = [];
        await this._load();
    }

    onSearch(ev) {
        clearTimeout(this._st);
        const val = ev.target.value;
        this._st = setTimeout(async () => {
            this.state.searchQuery = val;
            await this._load();
        }, 300);
    }

    cellValue(record, col) {
        const v = record[col.field];
        if (v === false || v === undefined || v === null) return "—";
        if (Array.isArray(v))  return v[1];
        if (typeof v === "boolean") return v ? "✓" : "—";
        if (LABELS[col.field]) return LABELS[col.field][v] || v;
        return String(v);
    }

    stateClass(record) {
        if (record.state === "paid")    return "rg_badge rg_badge_paid";
        if (record.state === "pending") return "rg_badge rg_badge_pending";
        return "";
    }
}

registry.category("actions").add("rigging.dashboard_client", RiggingDashboard);
