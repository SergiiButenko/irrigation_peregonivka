from devices.enums.rules import RulesPossibleState
from devices.enums.intervals import IntervalPossibleState
from devices.queries.rules import RulesQRS
from devices.queries.intervals import IntervalsQRS


class IntervalsCMD:

    @staticmethod
    async def cancel_interval(interval_id: str, current_user) -> None:
        await IntervalsQRS.set_interval_state(
            interval_id,
            IntervalPossibleState.CANCELED,
            current_user)

        rules = await RulesQRS.get_rules_by_interval_id(interval_id, only_active=True) 

        if rules is not None:
            for r in rules.__root__:
                await RulesQRS.set_rule_state(
                    r.id,
                    RulesPossibleState.CANCELED
                    )

        return await IntervalsQRS.get_interval(interval_id, current_user)
