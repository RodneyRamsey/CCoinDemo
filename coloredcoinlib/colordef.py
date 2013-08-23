class ColorDefinition(object):
    def __init__(self, color_id):
        self.color_id = color_id
        self.starting_height = None

    def is_special_tx(self, tx):
        return False

    def run_kernel(self, tx, in_colorstates):
        out_colorstates = []
        for o in tx.outputs:
            out_colorstates.append(None)
        return out_colorstates

class OBColorDefinition(ColorDefinition):
    def __init__(self, color_id, genesis):
        super(OBColorDefinition, self).__init__(color_id)
        self.genesis = genesis
        self.starting_height = genesis['height']

    def is_special_tx(self, tx):
        return (tx.hash == self.genesis['txhash'])

    def run_kernel(self, tx, in_colorstates):
        out_colorstates = []
        inp_index = 0
        cur_value = 0
        colored = False

        is_genesis = (tx.hash == self.genesis['txhash'])

        tx.ensure_input_values()

        for out_index in xrange(len(tx.outputs)):
            o = tx.outputs[out_index]
            if cur_value == 0:
                colored = True # reset
            while cur_value < o.value:
                cur_value += tx.inputs[inp_index].value
                if colored:
                    colored = (in_colorstates[inp_index] != None)
                inp_index += 1

            # genesis override:
            if is_genesis and (out_index == self.genesis['outindex']):
                colored = True

            if colored:
                out_colorstates.append((o.value, ''))
            else:
                out_colorstates.append(None)
        return out_colorstates
        
