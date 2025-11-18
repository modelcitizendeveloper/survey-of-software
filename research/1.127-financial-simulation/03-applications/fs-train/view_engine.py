#!/usr/bin/env python3
"""Pre-calculate all financial views from scenario data."""

from typing import Dict, List, Any, Tuple
from collections import defaultdict


class ViewEngine:
    """Calculate financial views from raw scenario data."""

    def __init__(self, scenario: Dict[str, Any]):
        self.scenario = scenario
        self.data = scenario['financial_data']
        self.months = self._get_months()
        self.views = {}

        # Pre-calculate all views
        self._calculate_all_views()

    def _get_months(self) -> List[str]:
        """Extract month keys from financial data in chronological order."""
        # Month order for sorting
        month_order = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                      'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

        revenue = self.data.get('revenue', {})
        months = list(revenue.keys())

        # Sort by month order
        return sorted(months, key=lambda m: month_order.index(m.lower())
                     if m.lower() in month_order else 999)

    def _calculate_all_views(self):
        """Pre-calculate all standard views."""
        self.views['default'] = self._calculate_default()
        self.views['%'] = self._calculate_percentage()
        self.views['mom'] = self._calculate_month_over_month()
        self.views['margin'] = self._calculate_margins()
        self.views['detail'] = self._calculate_detail()
        self.views['cash'] = self._calculate_cash_flow()

    def _calculate_default(self) -> Dict[str, Any]:
        """Calculate default view - absolute values."""
        revenue = self._get_line_item('revenue')
        cogs = self._get_line_item('cogs')
        opex_total = self._sum_opex()

        gross_profit = self._subtract(revenue, cogs)
        operating_income = self._subtract(gross_profit, opex_total)

        return {
            'revenue': revenue,
            'cogs': cogs,
            'gross_profit': gross_profit,
            'opex': opex_total,
            'operating_income': operating_income
        }

    def _calculate_percentage(self) -> Dict[str, Any]:
        """Calculate % of revenue view."""
        default = self.views.get('default', self._calculate_default())
        revenue = default['revenue']

        result = {}
        for key, values in default.items():
            result[key] = self._percentage_of(values, revenue)

        return result

    def _calculate_month_over_month(self) -> Dict[str, Any]:
        """Calculate month-over-month growth percentages."""
        default = self.views.get('default', self._calculate_default())

        result = {}
        for key, values in default.items():
            result[key] = self._mom_growth(values)

        # Add detailed opex breakdown
        opex = self.data.get('opex', {})
        result['opex_detail'] = {}
        for category, values in opex.items():
            result['opex_detail'][category] = self._mom_growth(values)

        return result

    def _calculate_margins(self) -> Dict[str, Any]:
        """Calculate margin analysis."""
        default = self.views.get('default', self._calculate_default())
        revenue = default['revenue']
        gross_profit = default['gross_profit']
        operating_income = default['operating_income']

        gross_margin = self._percentage_of(gross_profit, revenue)
        operating_margin = self._percentage_of(operating_income, revenue)

        return {
            'gross_margin': gross_margin,
            'operating_margin': operating_margin,
            'gross_trend': self._trend(gross_margin),
            'operating_trend': self._trend(operating_margin)
        }

    def _calculate_detail(self) -> Dict[str, Any]:
        """Calculate detailed line-item breakdown."""
        result = {
            'revenue': self._get_line_item('revenue'),
            'cogs': self._get_line_item('cogs'),
            'opex': self.data.get('opex', {})
        }
        return result

    def _calculate_cash_flow(self) -> Dict[str, Any]:
        """Calculate cash flow and runway."""
        default = self.views.get('default', self._calculate_default())
        operating_income = default['operating_income']
        starting_cash = self.data.get('cash', {}).get('starting', 0)

        # Calculate ending cash for each month
        cash_flow = {}
        current_cash = starting_cash

        for month in self.months:
            cash_flow[f'{month}_start'] = current_cash
            monthly_income = operating_income.get(month, 0)
            current_cash += monthly_income
            cash_flow[f'{month}_end'] = current_cash
            cash_flow[f'{month}_change'] = monthly_income

        return cash_flow

    # Helper methods

    def _get_line_item(self, key: str) -> Dict[str, float]:
        """Get a line item from financial data."""
        return self.data.get(key, {})

    def _sum_opex(self) -> Dict[str, float]:
        """Sum all operating expenses."""
        opex = self.data.get('opex', {})
        totals = defaultdict(float)

        for category, values in opex.items():
            for month, amount in values.items():
                totals[month] += amount

        return dict(totals)

    def _subtract(self, a: Dict[str, float], b: Dict[str, float]) -> Dict[str, float]:
        """Subtract two line items."""
        result = {}
        for month in self.months:
            result[month] = a.get(month, 0) - b.get(month, 0)
        return result

    def _percentage_of(self, numerator: Dict[str, float],
                       denominator: Dict[str, float]) -> Dict[str, float]:
        """Calculate percentage (numerator / denominator * 100)."""
        result = {}
        for month in self.months:
            denom = denominator.get(month, 0)
            if denom != 0:
                result[month] = (numerator.get(month, 0) / denom) * 100
            else:
                result[month] = 0
        return result

    def _mom_growth(self, values: Dict[str, float]) -> Dict[str, float]:
        """Calculate month-over-month growth percentage."""
        result = {}
        months_list = self.months

        for i in range(1, len(months_list)):
            prev_month = months_list[i-1]
            curr_month = months_list[i]

            prev_val = values.get(prev_month, 0)
            curr_val = values.get(curr_month, 0)

            if prev_val != 0:
                growth = ((curr_val - prev_val) / prev_val) * 100
                result[f'{prev_month}→{curr_month}'] = growth
            else:
                result[f'{prev_month}→{curr_month}'] = 0

        return result

    def _trend(self, values: Dict[str, float]) -> str:
        """Determine trend direction (↑, ↓, →)."""
        months_list = self.months
        if len(months_list) < 2:
            return "→"

        first = values.get(months_list[0], 0)
        last = values.get(months_list[-1], 0)

        diff = last - first
        if abs(diff) < 0.5:  # Essentially flat
            return "→"
        elif diff > 0:
            return "↑"
        else:
            return "↓"

    def get_view(self, view_name: str) -> Dict[str, Any]:
        """Get a pre-calculated view by name.

        Args:
            view_name: One of 'default', '%', 'mom', 'margin', 'detail', 'cash'

        Returns:
            View data dictionary
        """
        return self.views.get(view_name, self.views['default'])

    def format_view(self, view_name: str) -> str:
        """Format a view as terminal-friendly text.

        Args:
            view_name: View to format

        Returns:
            Formatted string for terminal display
        """
        view = self.get_view(view_name)

        if view_name == 'default':
            return self._format_default_view(view)
        elif view_name == '%':
            return self._format_percentage_view(view)
        elif view_name == 'mom':
            return self._format_mom_view(view)
        elif view_name == 'margin':
            return self._format_margin_view(view)
        elif view_name == 'detail':
            return self._format_detail_view(view)
        elif view_name == 'cash':
            return self._format_cash_view(view)
        else:
            return str(view)

    def _format_default_view(self, view: Dict[str, Any]) -> str:
        """Format default view with absolute values."""
        lines = ["── Income Statement ────────────────────────"]

        # Header
        header = f"{'':25}"
        for month in self.months:
            header += f"{month.capitalize():>10}"
        lines.append(header)
        lines.append("")

        # Line items
        items = [
            ('Revenue', 'revenue'),
            ('COGS', 'cogs'),
            ('Gross Profit', 'gross_profit'),
            ('Operating Expenses', 'opex'),
            ('Operating Income', 'operating_income')
        ]

        for label, key in items:
            line = f"{label:25}"
            for month in self.months:
                value = view[key].get(month, 0)
                line += f"${value:>9,.0f}"
            lines.append(line)

        return "\n".join(lines)

    def _format_percentage_view(self, view: Dict[str, Any]) -> str:
        """Format percentage of revenue view."""
        lines = ["── % of Revenue ────────────────────────────"]

        # Header
        header = f"{'':25}"
        for month in self.months:
            header += f"{month.capitalize():>10}"
        lines.append(header)
        lines.append("")

        items = [
            ('Revenue', 'revenue'),
            ('COGS', 'cogs'),
            ('Gross Profit', 'gross_profit'),
            ('Operating Expenses', 'opex'),
            ('Operating Income', 'operating_income')
        ]

        for label, key in items:
            line = f"{label:25}"
            for month in self.months:
                value = view[key].get(month, 0)
                line += f"{value:>9.1f}%"
            lines.append(line)

        return "\n".join(lines)

    def _format_mom_view(self, view: Dict[str, Any]) -> str:
        """Format month-over-month growth view."""
        lines = ["── Month-over-Month Growth (%) ─────────────"]

        # Get growth keys (e.g., "jan→feb")
        sample = view.get('revenue', {})
        growth_keys = sorted(sample.keys())

        # Header
        header = f"{'':25}"
        for key in growth_keys:
            header += f"{key:>12}"
        lines.append(header)
        lines.append("")

        items = [
            ('Revenue', 'revenue'),
            ('COGS', 'cogs'),
            ('Gross Profit', 'gross_profit'),
            ('Operating Expenses', 'opex'),
            ('Operating Income', 'operating_income')
        ]

        for label, key in items:
            line = f"{label:25}"
            for growth_key in growth_keys:
                value = view[key].get(growth_key, 0)
                line += f"{value:>11.1f}%"
            lines.append(line)

        # Add opex detail if available
        if 'opex_detail' in view:
            lines.append("")
            lines.append("OpEx Detail:")
            for category, growth in view['opex_detail'].items():
                line = f"  {category.capitalize():23}"
                for growth_key in growth_keys:
                    value = growth.get(growth_key, 0)
                    line += f"{value:>11.1f}%"
                lines.append(line)

        return "\n".join(lines)

    def _format_margin_view(self, view: Dict[str, Any]) -> str:
        """Format margin analysis view."""
        lines = ["── Margin Trends ───────────────────────────"]

        # Header
        header = f"{'':25}"
        for month in self.months:
            header += f"{month.capitalize():>10}"
        header += "  Trend"
        lines.append(header)
        lines.append("")

        items = [
            ('Gross Margin', 'gross_margin', 'gross_trend'),
            ('Operating Margin', 'operating_margin', 'operating_trend')
        ]

        for label, key, trend_key in items:
            line = f"{label:25}"
            for month in self.months:
                value = view[key].get(month, 0)
                line += f"{value:>9.1f}%"
            line += f"    {view[trend_key]}"
            lines.append(line)

        return "\n".join(lines)

    def _format_detail_view(self, view: Dict[str, Any]) -> str:
        """Format detailed line-item breakdown."""
        lines = ["── Detailed P&L ────────────────────────────"]

        # Header
        header = f"{'':25}"
        for month in self.months:
            header += f"{month.capitalize():>11}"
        lines.append(header)
        lines.append("")

        # Revenue
        lines.append("Revenue")
        revenue = view['revenue']
        line = f"  {'Total':23}"
        for month in self.months:
            value = revenue.get(month, 0)
            line += f" ${value:>9,.0f}"
        lines.append(line)
        lines.append("")

        # COGS
        lines.append("Cost of Goods Sold")
        cogs = view['cogs']
        line = f"  {'Total':23}"
        for month in self.months:
            value = cogs.get(month, 0)
            line += f" ${value:>9,.0f}"
        lines.append(line)
        lines.append("")

        # OpEx detail
        lines.append("Operating Expenses")
        opex = view.get('opex', {})

        # Show individual categories
        for category, values in sorted(opex.items()):
            line = f"  {category.capitalize():23}"
            for month in self.months:
                value = values.get(month, 0)
                line += f" ${value:>9,.0f}"
            lines.append(line)

        # Show total
        total_line = f"  {'Total OpEx':23}"
        for month in self.months:
            total = 0
            for category, values in opex.items():
                total += values.get(month, 0)
            total_line += f" ${total:>9,.0f}"
        lines.append(total_line)

        return "\n".join(lines)

    def _format_cash_view(self, view: Dict[str, Any]) -> str:
        """Format cash flow and runway view."""
        lines = ["── Cash Flow Analysis ──────────────────────"]

        # Header
        header = f"{'':25}"
        for month in self.months:
            header += f"{month.capitalize():>11}"
        lines.append(header)
        lines.append("")

        # Starting cash row
        line = f"{'Starting Cash':25}"
        for month in self.months:
            start_key = f'{month}_start'
            value = view.get(start_key, 0)
            line += f" ${value:>9,.0f}"
        lines.append(line)

        # Cash from operations row
        line = f"{'Cash from Ops':25}"
        for month in self.months:
            change_key = f'{month}_change'
            change = view.get(change_key, 0)
            if change >= 0:
                line += f" +${change:>8,.0f}"
            else:
                line += f" ${change:>9,.0f}"
        lines.append(line)

        # Ending cash row
        line = f"{'Ending Cash':25}"
        for month in self.months:
            end_key = f'{month}_end'
            value = view.get(end_key, 0)
            line += f" ${value:>9,.0f}"
        lines.append(line)

        return "\n".join(lines)
