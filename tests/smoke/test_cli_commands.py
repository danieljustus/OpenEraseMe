from __future__ import annotations

from .conftest import assert_ok, invoke


class TestVersion:
    def test_version_output(self):
        result = invoke("version")
        assert_ok(result)
        assert "OpenEraseMe" in result.stdout

    def test_version_contains_number(self):
        result = invoke("version")
        assert_ok(result)
        assert any(c.isdigit() for c in result.stdout)


class TestHelp:
    def test_help_shows_commands(self):
        result = invoke("--help")
        assert_ok(result)
        assert "init-profile" in result.stdout

    def test_help_no_args(self):
        result = invoke("--help")
        assert_ok(result)


class TestOutputFormat:
    def test_json_from_plan_create(self, seeded_db):
        result = invoke("--output", "json", "plan", "create", "--campaign", "fmt-test")
        import json
        assert_ok(result)
        data = json.loads(result.stdout)
        assert data["campaign_id"] == "fmt-test"

    def test_json_from_tick(self, seeded_db):
        result = invoke("--output", "json", "tick", "--dry-run")
        import json
        assert_ok(result)
        data = json.loads(result.stdout)
        assert "total_actions" in data


class TestNonExistentCommand:
    def test_unknown_command_fails(self):
        result = invoke("nonexistent-command")
        assert result.exit_code != 0


class TestBrokersList:
    def test_list_default_returns_brokers(self):
        result = invoke("brokers", "list")
        assert_ok(result)
        assert "broker(s)" in result.stdout

    def test_list_json_shape(self):
        from .conftest import assert_json_output

        result = invoke("--output", "json", "brokers", "list")
        data = assert_json_output(result)
        assert data["schema_version"] == 1
        assert "count" in data
        assert "brokers" in data
        assert data["count"] == len(data["brokers"])
        assert data["filters"]["include_disabled"] is False

    def test_list_filter_by_priority(self):
        from .conftest import assert_json_output

        result = invoke("--output", "json", "brokers", "list", "--priority", "high")
        data = assert_json_output(result)
        for broker in data["brokers"]:
            assert broker["priority"] == "high"

    def test_list_filter_by_jurisdiction(self):
        from .conftest import assert_json_output

        result = invoke("--output", "json", "brokers", "list", "--jurisdiction", "DE")
        data = assert_json_output(result)
        for broker in data["brokers"]:
            assert "DE" in broker["jurisdictions"]

    def test_list_excludes_disabled_by_default(self):
        from .conftest import assert_json_output

        result = invoke("--output", "json", "brokers", "list")
        data = assert_json_output(result)
        for broker in data["brokers"]:
            assert broker["disabled"] is False, (
                f"Disabled broker {broker['id']} leaked into default list"
            )

    def test_list_include_disabled(self):
        from .conftest import assert_json_output

        result_default = invoke("--output", "json", "brokers", "list")
        result_all = invoke("--output", "json", "brokers", "list", "--include-disabled")
        default = assert_json_output(result_default)
        full = assert_json_output(result_all)
        assert full["count"] >= default["count"]
        disabled = [b for b in full["brokers"] if b["disabled"]]
        assert disabled, "registry should have at least one disabled broker for this test"


class TestBrokersShow:
    def test_show_known_broker_text(self):
        result = invoke("brokers", "show", "acxiom-eu")
        assert_ok(result)
        assert "Acxiom" in result.stdout
        assert "acxiom-eu" in result.stdout

    def test_show_known_broker_json(self):
        from .conftest import assert_json_output

        result = invoke("--output", "json", "brokers", "show", "acxiom-eu")
        data = assert_json_output(result)
        assert data["schema_version"] == 1
        assert data["broker"]["id"] == "acxiom-eu"
        assert data["broker"]["name"] == "Acxiom (EU)"

    def test_show_disabled_broker_still_visible(self):
        """`show` is informational — it shows disabled brokers too."""
        from .conftest import assert_json_output

        result = invoke("--output", "json", "brokers", "show", "beenverified-us")
        data = assert_json_output(result)
        assert data["broker"]["id"] == "beenverified-us"
        assert data["broker"]["disabled"] is True

    def test_show_unknown_broker_exits_nonzero(self):
        result = invoke("brokers", "show", "this-broker-does-not-exist")
        assert result.exit_code != 0
