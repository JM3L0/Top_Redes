package tests.validation;


import domain.LoadBalancerProxy;
import domain.Source;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Estes estudos de caso são apenas ilustrativos e de testes.
 * Estes estudos de caso não devem ser executados da maneira que está aqui (monolítico).
 * Você deve executar os componentes separadamente de forma distribuída em máquinas vísicas ou VMs e contêineres.
 *  *  @author Airton
 */
public class LocalTest_Services {

	public static void main(String[] args) {
		executeStage();
	}

	private static void executeStage() {

		String path = resolveValidationDir();
		String loadBalancerJsonPath1 = path + "loadbalancer1.properties";
		String loadBalancerJsonPath2 = path + "loadbalancer2.properties";

		new LoadBalancerProxy(loadBalancerJsonPath2).start();

		new LoadBalancerProxy(loadBalancerJsonPath1).start();

		new Source(path).start();
	}

	/**
	 * user.dir may be the repo root (e.g. "Trabalho 4") or pasid-validator-main.
	 */
	private static String resolveValidationDir() {
		Path cwd = Paths.get(System.getProperty("user.dir"));
		Path direct = cwd.resolve("src/tests/validation");
		if (Files.isRegularFile(direct.resolve("loadbalancer2.properties"))) {
			return direct.toString().replace('\\', '/') + "/";
		}
		Path nested = cwd.resolve("pasid-validator-main/src/tests/validation");
		if (Files.isRegularFile(nested.resolve("loadbalancer2.properties"))) {
			return nested.toString().replace('\\', '/') + "/";
		}
		throw new IllegalStateException(
				"Could not find src/tests/validation/loadbalancer2.properties under " + cwd
						+ " or " + nested);
	}
}

