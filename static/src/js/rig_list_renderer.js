/** @odoo-module **/

import { useState, onWillUpdateProps } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListRenderer } from "@web/views/list/list_renderer";

const FILTERABLE_TYPES = ["char", "text", "many2one", "selection"];

export class RigListRenderer extends ListRenderer {
    setup() {
        super.setup();

        this.columnFilters = useState({});
        this.searchDomain = this.props.list.domain;
        this.lastSetDomain = this.props.list.domain;

        onWillUpdateProps((nextProps) => {
            const newDomain = nextProps.list.domain;
            if (JSON.stringify(newDomain) !== JSON.stringify(this.lastSetDomain)) {
                this.searchDomain = newDomain;
                if (this.hasActiveFilters()) {
                    const combined = this.getCombinedDomain();
                    this.lastSetDomain = combined;
                    nextProps.list.model.load({ domain: combined });
                } else {
                    this.lastSetDomain = newDomain;
                }
            }
        });
    }

    isFilterableColumn(column) {
        if (column.type !== "field" || column.widget === "handle") {
            return false;
        }
        const field = this.props.list.fields[column.name];
        return field && FILTERABLE_TYPES.includes(field.type);
    }

    getSelectionOptions(column) {
        const field = this.props.list.fields[column.name];
        return (field && field.selection) || [];
    }

    hasActiveFilters() {
        return Object.values(this.columnFilters).some((value) => value);
    }

    getCombinedDomain() {
        const leaves = [];
        for (const [fieldName, value] of Object.entries(this.columnFilters)) {
            if (value) {
                leaves.push([fieldName, "ilike", value]);
            }
        }
        return [...this.searchDomain, ...leaves];
    }

    onColumnFilterInput(fieldName, ev) {
        this.columnFilters[fieldName] = ev.target.value;
        clearTimeout(this._filterTimeout);
        this._filterTimeout = setTimeout(() => {
            const combined = this.getCombinedDomain();
            this.lastSetDomain = combined;
            this.props.list.model.load({ domain: combined });
        }, 400);
    }

    onColumnFilterChange(fieldName, ev) {
        this.columnFilters[fieldName] = ev.target.value;
        clearTimeout(this._filterTimeout);
        const combined = this.getCombinedDomain();
        this.lastSetDomain = combined;
        this.props.list.model.load({ domain: combined });
    }

    // These columns belong to the rig itself (no internal link of their
    // own), so clicking them opens the current rig's form view.
    static OPEN_RIG_FIELDS = ["number", "usage_type", "reserve_last_repack"];

    async onCellClicked(record, column, ev, newWindow) {
        if (
            column.type === "field" &&
            RigListRenderer.OPEN_RIG_FIELDS.includes(column.name)
        ) {
            this.props.openRecord(record, { newWindow });
            return;
        }
        return super.onCellClicked(record, column, ev, newWindow);
    }
}

RigListRenderer.template = "rigging.ListRenderer";

registry.category("views").add("rigging_list", {
    ...listView,
    Renderer: RigListRenderer,
});
