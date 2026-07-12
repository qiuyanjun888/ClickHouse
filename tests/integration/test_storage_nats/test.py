import pytest

from helpers.cluster import ClickHouseCluster

cluster = ClickHouseCluster(__file__)
node = cluster.add_instance(
    "node",
    main_configs=["configs/named_collection.xml"],
    with_nats=True,
    stay_alive=True,
    with_remote_database_disk=False,
)


@pytest.fixture(scope="module", autouse=True)
def started_cluster():
    try:
        cluster.start()
        yield cluster
    finally:
        cluster.shutdown()


def test_named_collection_without_table_settings_survives_restart():
    node.query(
        """
        CREATE TABLE nats_empty_settings (x UInt8)
        ENGINE = NATS(
            nats_default,
            nats_subjects = 'issue_107750',
            nats_format = 'JSONEachRow'
        )
        """
    )

    metadata_path = node.query(
        "SELECT metadata_path FROM system.tables "
        "WHERE database = 'default' AND name = 'nats_empty_settings'"
    ).strip()
    metadata = node.exec_in_container(["cat", metadata_path])
    assert not metadata.rstrip().endswith("SETTINGS")

    node.restart_clickhouse()

    assert "NATS" in node.query("SHOW CREATE TABLE nats_empty_settings")
