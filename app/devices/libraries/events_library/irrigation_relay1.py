class IrrigationRelay1:

    class WaterLine:
        def set_state(state: dict):
            if state.expepted_state == 1:
                #turn on valve
                #sleep 1
                # turn on pump
                pass
            
            if state.expepted_state == 0:
                #turn of pump
                # sleep 1
                #turn of valve
                pass
            