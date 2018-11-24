import pytest


class TestAtomic:

    def test_fuc_atomic(self, testdir):
        testdir.makeini(f'''
            [pytest]
            addopts: 
            [atomic]
            enable: true
            electronic: true
        ''')

        testdir.makepyfile(f'''
            import pytest
            @pytest.mark.atomic
            def test_1():
                assert 0
            def test_2():
                assert 0
            def test_3():
                assert 0
        ''')

        result = testdir.runpytest('-v')
        result.stdout.fnmatch_lines([
            '*test_1*FAILED*',
            '*test_2*SKIPPED*',
            '*test_3*SKIPPED*',
        ])

    def test_fuc_atomic_electronic(self, testdir):
        testdir.makeini(f'''
            [pytest]
            addopts: -v
            [atomic]
            enable: true
            electronic: true
        ''')

        testdir.makepyfile(f'''
            import pytest
            @pytest.mark.atomic
            def test_1():
                assert 0
            def test_2():
                assert 0
            @pytest.mark.electronic
            def test_3():
                assert 0
            def test_4():
                assert 0
            def test_5():
                assert 0
        ''')

        result = testdir.runpytest('-v')
        result.stdout.fnmatch_lines([
            '*test_1*FAILED*',
            '*test_2*SKIPPED*',
            '*test_3*FAILED*',
            '*test_4*SKIPPED*',
            '*test_5*SKIPPED*',
        ])

    def test_fuc_multi_atomic_electronic(self, testdir):
        testdir.makeini(f'''
            [pytest]
            addopts: -v
            [atomic]
            enable: true
            electronic: true
           ''')

        testdir.makepyfile(f'''
            import pytest
            @pytest.mark.atomic
            def test_1():
               assert 0
            def test_2():
               assert 0
            @pytest.mark.electronic
            def test_3():
               assert 0
            @pytest.mark.atomic
            def test_4():
               assert 0
            def test_5():
               assert 0
            @pytest.mark.electronic
            def test_6():
               assert 0            
            def test_7():
               assert 0            
            @pytest.mark.atomic
            def test_8():
               assert 1
            def test_9():
               assert 1
           ''')

        result = testdir.runpytest('-v')
        result.stdout.fnmatch_lines([
            '*test_1*FAILED*',
            '*test_2*SKIPPED*',
            '*test_3*FAILED*',
            '*test_4*FAILED*',
            '*test_5*SKIPPED*',
            '*test_6*FAILED*',
            '*test_7*SKIPPED*',
            '*test_8*PASSED*',
            '*test_9*PASSED*',
        ])

    def test_cls_atomic_electronic(self, testdir):
        testdir.makeini(f'''
        [pytest]
        addopts: -v
        [atomic]
        enable: true
        electronic: true
        ''')

        testdir.makepyfile(f'''
        import pytest
        class TestCls:
            @pytest.mark.atomic
            def test_1(self):
                assert 0

            @pytest.mark.electronic
            def test_2(self):
                assert 1

            def test_3(self):
                assert 0

            @pytest.mark.electronic
            def test_4(self):
                assert 1

            def test_5(self):
                assert 0
        ''')
        result = testdir.runpytest('-v')
        result.stdout.fnmatch_lines([
            '*test_1*FAILED*',
            '*test_2*PASSED*',
            '*test_3*SKIPPED*',
            '*test_4*PASSED*',
            '*test_5*SKIPPED*',
        ])

    @pytest.mark.parametrize('electronic', ['true', 'false'])
    def test_multi_scope_atomic(self, electronic, testdir):
        testdir.makeini(f'''
        [pytest]
        addopts: -v
        [atomic]
        enable: true
        electronic: {electronic}
        ''')

        testdir.makepyfile(f'''
        import pytest

        @pytest.mark.atomic
        def test_fn1():
            assert 0

        def test_fn2():
            assert 0

        class TestCls:
            @pytest.mark.atomic
            def test_1(self):
                assert 0
            @pytest.mark.electronic
            def test_2(self):
                assert 1
            def test_3(self):
                assert 0
            @pytest.mark.electronic
            def test_4(self):
                assert 1
            def test_5(self):
                assert 0

        def test_fn3():
            assert 0
        @pytest.mark.atomic
        def test_fn4():
            assert 0
        def test_fn5():
            assert 0
        ''')
        result = testdir.runpytest('-v')
        if electronic == 'true':
            result.stdout.fnmatch_lines([
                '*test_fn1*FAILED*',
                '*test_fn2*SKIPPED*',
                '*test_1*FAILED*',
                '*test_2*PASSED*',
                '*test_3*SKIPPED*',
                '*test_4*PASSED*',
                '*test_5*SKIPPED*',
                '*test_fn3*SKIPPED*',
                '*test_fn4*FAILED*',
                '*test_fn5*SKIPPED*',
            ])
        else:
            result.stdout.fnmatch_lines([
                '*test_fn1*FAILED*',
                '*test_fn2*SKIPPED*',
                '*test_1*FAILED*',
                '*test_2*SKIPPED*',
                '*test_3*SKIPPED*',
                '*test_4*SKIPPED*',
                '*test_5*SKIPPED*',
                '*test_fn3*SKIPPED*',
                '*test_fn4*FAILED*',
                '*test_fn5*SKIPPED*',
            ])

if __name__ == '__main__':
    pytest.main(['-v'])
