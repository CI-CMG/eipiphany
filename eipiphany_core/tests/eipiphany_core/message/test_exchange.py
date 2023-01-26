from ....src.eipiphany_core.message.exchange import Exchange


class TestExchange(object):

  def test_exchange(self):
    exchange = Exchange('foo')
    assert exchange.body == 'foo'
    assert Exchange('foo').set_body('bar').body == 'bar'
    exchange = Exchange('foo')
    exchange.body = 'bar'
    assert exchange.body == 'bar'
    exchange = Exchange('foo').set_body('bar').set_header('pet', 'dog').set_header('food', 'hot dog')
    exchange.headers['job'] = 'code monkey'
    assert exchange.headers['pet'] == 'dog'
    assert exchange.headers['job'] == 'code monkey'
    assert exchange.headers['food'] == 'hot dog'

