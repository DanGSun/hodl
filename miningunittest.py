import mining
import block
import cryptogr as cg
import unittest


my_keys = cg.gen_keys()
your_pub_key = cg.gen_keys()[1]
class MiningUnittest(unittest.TestCase):
    def test_pow(self):
        bch = block.Blockchain()
        bch.new_block([my_keys[1], my_keys[1], your_pub_key])
        bch.new_block([my_keys[1], my_keys[1], your_pub_key])
        bch.new_transaction(my_keys[1], [(0, 0)], [your_pub_key, my_keys[1]], [0.5, 0.25], 'signing', my_keys[0])
        bch.new_transaction(my_keys[1], [(0, 0)], [your_pub_key, my_keys[1]], [0.05, 0.95], 'signing', my_keys[0])
        bch.new_transaction(my_keys[1], [(0, 0)], [your_pub_key, my_keys[1]], [0.05, 0.95], 'signing', my_keys[0])
        bch.new_transaction(my_keys[1], [(0, 0)], [your_pub_key, my_keys[1]], [0.05, 0.95], 'signing', my_keys[0])
        bch.new_transaction(my_keys[1], [(0, 0)], [your_pub_key, my_keys[1]], [0.05, 0.95], 'signing', my_keys[0])
        n, t, h = mining.pow_mine(bch, 900000000000000000000000000000000000, my_keys[1])
        print(n, t, h)

    def test_poc(self):
        bch = block.Blockchain()
        bch.new_block([my_keys[1], my_keys[1], your_pub_key])
        bch.new_block([my_keys[1], my_keys[1], your_pub_key])
        bch.new_transaction(my_keys[1], [(0, 0)], [your_pub_key, my_keys[1]], [0.5, 0.25], 'signing', my_keys[0])
        bch.new_transaction(my_keys[1], [(0, 0)], [your_pub_key, my_keys[1]], [0.05, 0.95], 'signing', my_keys[0])
        bch.new_transaction(my_keys[1], [(0, 0)], [your_pub_key, my_keys[1]], [0.05, 0.95], 'signing', my_keys[0])
        bch.new_transaction(my_keys[1], [(0, 0)], [your_pub_key, my_keys[1]], [0.05, 0.95], 'signing', my_keys[0])
        bch.new_transaction(my_keys[1], [(0, 0)], [your_pub_key, my_keys[1]], [0.05, 0.95], 'signing', my_keys[0])
        xs = mining.poc_mine(1000, bch, my_keys[1])
        bch[-1].pocminers.append([1000, my_keys[1], xs])
        print(len(xs), xs)

    def test_mining(self):
        bch = block.Blockchain()
        bch.new_block([my_keys[1], my_keys[1], your_pub_key])
        bch.new_transaction(my_keys[1], [(0, 0)], [your_pub_key, my_keys[1]], [0.5, 0.25], 'signing', my_keys[0])
        bch.new_transaction(my_keys[1], [(0, 0)], [your_pub_key, my_keys[1]], [0.05, 0.95], 'signing', my_keys[0])
        bch.new_transaction(my_keys[1], [(0, 0)], ['mining', my_keys[1]], [0.05, 0.95], 'signing', my_keys[0])
        bch.new_transaction(my_keys[1], [(0, 0)], ['mining', my_keys[1]], [0.05, 0.95], 'signing', my_keys[0])
        bch.new_transaction(my_keys[1], [(0, 0)], ['mining', my_keys[1]], [0.05, 0.95], 'signing', my_keys[0])
        n = 1000
        xs = mining.poc_mine(n, bch, my_keys[1])
        bch.add_miner([n, my_keys[1], xs], 'poc')
        bch.add_miner([n, my_keys[1], xs], 'poc')
        bch.add_miner([n, my_keys[1], xs], 'poc')
        n, t, h = mining.pow_mine(bch, 90000000000000000000000000000000000, my_keys[1])
        bch.add_miner([int(h), n, my_keys[1], t], 'pow')
        bch.add_miner([int(h), n, my_keys[1], t], 'pow')
        bch.add_miner([int(h), n, my_keys[1], t], 'pow')
        bl = block.Block(n, [my_keys[1]], bch, [], [], t)
        b = mining.mine(bch)
        bch.append(b)
        print('n', bch[-1].n)
        self.assertTrue(mining.validate(bch, -1))


if __name__ == '__main__':
    unittest.main()
