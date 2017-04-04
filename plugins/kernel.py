import plugin as p

class KernelPlugin(p.Plugin):
    def checkParms(self, plugins_output):
        '''Check Kernel Parameters'''
        parms = {
            'net.ipv4.conf.default.rp_filter': 1,
            'net.ipv4.conf.all.rp_filter': 1,
            'net.ipv4.conf.default.accept_source_route': 0,
            'net.ipv4.conf.all.accept_source_route': 0,
            'fs.protected_hardlinks': 1,
            'fs.protected_symlinks': 1
        }

        for k, v in parms.items():
            self._check_kernel_parm(k, v)